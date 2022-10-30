from automator import AddonBase, cli_command
from Arknights.flags import *
from .common import CommonAddon
class QuestAddon(AddonBase):
    def clear_task(self):
        import imgreco.main
        import imgreco.task
        self.logger.debug("helper.clear_task")
        self.logger.info("Collecting daily mission rewards")
        self.addon(CommonAddon).back_to_main()
        screenshot = self.screenshot()
        self.logger.info('Entering mission UI')
        self.tap_quadrilateral(imgreco.main.get_task_corners(screenshot))
        self.delay(SMALL_WAIT)
        screenshot = self.screenshot()

        hasbeginner = imgreco.task.check_beginners_task(screenshot)
        if hasbeginner:
            self.logger.info('Found pinboard missions, switching to daily missions')
            self.tap_rect(imgreco.task.get_daily_task_rect(screenshot, hasbeginner))
            self.delay(TINY_WAIT)
            screenshot = self.screenshot()
        self.clear_task_worker()
        self.logger.info('Switching to weekly missions') #默认进入见习任务或每日任务，因此无需检测，直接切换即可
        self.tap_rect(imgreco.task.get_weekly_task_rect(screenshot, hasbeginner))
        self.clear_task_worker()

    def clear_task_worker(self):
        import imgreco.common
        import imgreco.task
        screenshot = self.screenshot()
        kickoff = True
        while True:
            if imgreco.common.check_nav_button(screenshot) and not imgreco.task.check_collectable_reward(screenshot):
                self.logger.info("Rewards have been collected")
                break
            if kickoff:
                self.logger.info('Start receiving rewards')
                kickoff = False
            self.tap_rect(imgreco.task.get_collect_reward_button_rect(self.viewport))
            screenshot = self.screenshot(cached=False)

    @cli_command('collect')
    def cli_collect(self, argv):
        """
        collect
        Collect daily/weekly mission rewards
        """
        with self.helper.frontend.context:
            self.clear_task()
        return 0
