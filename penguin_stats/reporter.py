from __future__ import annotations
import logging
from dataclasses import dataclass
import app
from resources.event import EXTRA_KNOWN_ITEMS, event_preprocess
import requests
from requests_cache import CachedSession
from urllib.parse import urljoin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from imgreco.end_operation import EndOperationResult
from .penguin_schemas import Item, Stage, SingleReportRequest, ArkDrop

logger = logging.getLogger('PenguinReporter')

REPORT_SOURCE = 'ArknightsAutoHelper'

API_BASE = {
    'global': 'https://penguin-stats.io/',
    'cn': 'https://penguin-stats.cn/',
}
def api_endpoint(path):
    return urljoin(API_BASE[app.config.combat.penguin_stats.endpoint], path)

def _check_in_bound(bound, num):
    result = bound['lower'] <= num <= bound['upper'] 
    if num in bound.get('exceptions', []):
        return False
    return result


class ReportResult:
    pass
@dataclass
class ReportResultOk(ReportResult):
    report_hash: str
ReportResult.Ok = ReportResultOk
ReportResult.NothingToReport = ReportResult()
ReportResult.NotReported =ReportResult()

class PenguinStatsReporter:
    GROUP_NAME_TO_TYPE_MAP = {
        'Regular Drops': 'NORMAL_DROP',
        'Special Drops': 'SPECIAL_DROP',
        'Extra Drops': 'EXTRA_DROP',
        'Lucky Drops': 'FURNITURE',
    }

    def __init__(self):
        self.logged_in = False
        self.initialized = None
        self.noop = False
        self.stage_map: dict[str, Stage] = {}
        self.item_map: dict[str, Item] = {}
        self.item_name_map: dict[str, Item] = {}
        self.cache_client = CachedSession(backend='memory', cache_control=True)
        self.client = requests.session()

    
    def set_login_state_with_response(self, response: requests.Response):
        if userid := response.headers.get('X-Penguin-Set-Penguinid', None):
            self.logged_in = True
            self.client.headers['Authorization'] = f'PenguinID {userid}'
            logger.debug('set headers in session: %r', self.client.headers)
        return userid

    def try_login(self, userid):
        if self.logged_in:
            return True
        try:
            logger.info('Signing in to Penguin Statistics, userID=%s', userid)
            resp = self.client.post(api_endpoint('/PenguinStats/api/v2/users'), data=str(userid))
            resp.raise_for_status()
        except: 
            logger.error('Login failed', exc_info=1)
            return False
        self.set_login_state_with_response(resp)
        return True

    def initialize(self):
        if self.initialized is not None:
            return self.initialized
        if app.version == 'UNKNOWN':
            logger.warn('Program version unavailable, please download the source code using git')
            logger.warn('Reporting has been disabled to avoid statistical bias')
            self.noop = True
            self.initialized = False
            return True
        try:
            logger.info('Loading Penguin Statistics resources...')
            self.update_penguin_data()
            self.initialized = True
        except:
            logger.error('Error loading Penguin Statistics resources', exc_info=True)
            self.initialized = False
        return self.initialized

    def set_penguin_data(self, stages: list[Stage], items: list[Item]):
        name_to_id_map = {}
        for s in stages:
            self.stage_map[s['code']] = s
        for i in items:
            if i.get('itemType') == 'RECRUIT_TAG' or not i['existence'][app.config.server]['exist']:
                continue
            self.item_map[i['itemId']] = i
            self.item_name_map[i['name']] = i
            name_to_id_map[i['name']] = i['itemId']
        import imgreco.itemdb
        unrecognized_items = set(self.item_map.keys()) - set(imgreco.itemdb.dnn_items_by_item_id.keys()) - set(EXTRA_KNOWN_ITEMS)
        extra_recognized_item_names = imgreco.itemdb.resources_known_items.keys()
        extra_recognized_item_ids = set(name_to_id_map.get(name, None) for name in extra_recognized_item_names)
        extra_recognized_item_ids.remove(None)
        unrecognized_items.difference_update(extra_recognized_item_ids)
        if unrecognized_items:
            logger.warn('Unrecognized items were found in Penguin Statistics data: %s', ', '.join(unrecognized_items))
            logger.warn('Reporting has been disabled to avoid statistical bias')
            self.noop = True

    def update_penguin_data(self):
        stages_resp = self.cache_client.get(api_endpoint('/PenguinStats/api/v2/stages'))
        items_resp = self.cache_client.get(api_endpoint('/PenguinStats/api/v2/items'))
        if self.initialized and stages_resp.from_cache and items_resp.from_cache:
            return
        stages: list[Stage] = stages_resp.json()
        items: list[Item] = items_resp.json()
        self.set_penguin_data(stages, items)

    def report(self, recoresult: EndOperationResult):
        if self.initialize() == False or self.noop:
            return ReportResult.NotReported
        logger.info('Reporting drops to Penguin Statistics')
        if recoresult.stars != (True, True, True):
            logger.info('Only 3-star clears can be reported')
            return ReportResult.NotReported
        if recoresult.low_confidence:
            logger.info('Not reporting low-confidence results')
            return ReportResult.NotReported

        code = recoresult.operation

        self.update_penguin_data()
        if code not in self.stage_map:
            logger.info('Penguin Statistics do not have this level: %s', code)
            return ReportResult.NothingToReport
        stage = self.stage_map[code]

        if not stage.get('dropInfos'):
            logger.info('No drop information is available for %s, not reporting', code)
            return ReportResult.NothingToReport
        logger.debug('%r', stage['dropInfos'])
        if sum(1 for drop in stage['dropInfos'] if drop.get('itemId', None) != 'furni') == 0:
            logger.info('No drops for %s is available except furniture, not reporting', code)
            return ReportResult.NothingToReport

        itemgroups = recoresult.items
        exclude_from_validation = []

        flattenitems = [(groupname, item) for groupname, items in itemgroups for item in items]

        try:
            flattenitems = list(event_preprocess(recoresult.operation, flattenitems, exclude_from_validation))
            report_special_item = app.config.combat.penguin_stats.report_special_item
            for item in flattenitems:
                if item[1].item_type == 'special_report_item' and not report_special_item:
                    logger.error('Please go to Penguin Statistics to read reporting instructions, and change the '
                                 'reporting/report_special_items configuration key to true to report the drop after '
                                 'conditions are met')
                    raise RuntimeError('Special items are not reported.')
        except:
            logger.error('Error handling event items', exc_info=True)
            return ReportResult.NotReported
        typeddrops: list[ArkDrop] = []
        dropinfos = stage['dropInfos']
        for itemdef in flattenitems:
            groupname, item = itemdef
            if groupname == 'First Clear':
                logger.info('First clears cannot be reported')
                return ReportResult.NotReported
            if 'LMD' in groupname:
                continue
            if groupname == 'Lucky Drops':
                typeddrops.append(ArkDrop(dropType='FURNITURE', itemId='furni', quantity=1))
                continue

            droptype = PenguinStatsReporter.GROUP_NAME_TO_TYPE_MAP.get(groupname, None)
            if droptype is None:
                logger.warning("Not reporting drops in %s group", groupname)
                return ReportResult.NotReported

            if item.item_id in stage.get('recognitionOnly', []):
                logger.debug('Not reporting recognized items (recognitionOnly): %s', item.item_id)
                continue
            if item.item_type == 'special_report_item' and app.config.combat.penguin_stats.report_special_item:
                penguin_item = self.item_name_map.get(item.name, None)
            else:
                penguin_item = self.item_map.get(item.item_id, None)
            if penguin_item is None:
                logger.warning("%s is not in the list of Penguin Statistics items", item.name)
                return ReportResult.NotReported
            itemid = penguin_item['itemId']
            if itemdef not in exclude_from_validation:
                filterresult = [x for x in dropinfos if x.get('itemId', None) == itemid and x['dropType'] == droptype]
                if filterresult:
                    dropinfo4item = filterresult[0]
                    if not _check_in_bound(dropinfo4item['bounds'], item.quantity):
                        logger.error('Item %s does not meet Penguin Statistics validation rules', item)
                        return ReportResult.NotReported
                else:
                    logger.warning('Item is missing validation rules: %s: %r', groupname, item)
            typeddrops.append(ArkDrop(dropType=droptype, itemId=itemid, quantity=item.quantity))

        for groupinfo in dropinfos:
             if groupinfo.get('itemId', None) is None:
                kinds = sum(1 for x in typeddrops if x['dropType'] == groupinfo['dropType'])
                if not _check_in_bound(groupinfo['bounds'], kinds):
                    logger.error('The number of items (%d) in group %s does not meet Penguin Statistics validation rules', kinds, groupinfo['dropType'])
                    return ReportResult.NotReported

        from imgreco.itemdb import model_timestamp

        req = SingleReportRequest(
            drops=typeddrops,
            server='CN',
            stageId=stage['stageId'],
            source=REPORT_SOURCE,
            version=f'{app.version},ark_material@{model_timestamp // 1000}',
        )

        logger.debug('raw request: %r', req)

        if not self.logged_in:
            uid = app.config.combat.penguin_stats.uid
            if uid is not None:
                self.try_login(uid)
        try:
            # use cookie stored in session
            resp = self.client.post(api_endpoint('/PenguinStats/api/v2/report'), json=req)
            resp.raise_for_status()
            if not self.logged_in:
                userid = self.set_login_state_with_response(resp)
                if userid is not None:
                    logger.info('Penguin Statistics User ID: %s', userid)
                    app.config.combat.penguin_stats.uid = userid
                    app.save()
                    logger.info('Written to configuration file.')
            return ReportResult.Ok(resp.json().get('reportHash'))
        except:
            logger.error('Report failed', exc_info=True)
        return ReportResult.NotReported
