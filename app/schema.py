from typing import Literal
from .schemadef import *


class ControllerConfig(Schema):
    screenshot_method = EnumField(
        ["aah-agent", "aosp-screencap"],
        "aah-agent",
        "screenshot_method",
        "aah-agent: screenshot is faster and supports wm size dynamic resolution adjustment, but some emulators are incompatible (screenshot is black or stuck)\naosp-screencap: uses AOSP screencap command, slower, but good compatibility.",
    )
    input_method = EnumField(
        ["aah-agent", "aosp-input"],
        "aah-agent",
        "input_injection_method",
        "aah-agent: use aah-agent; \naosp-input: use input command",
    )
    screenshot_transport = EnumField(
        ["auto", "adb", "vm_network"],
        "auto",
        "screenshot transport method",
        "auto: try vm_network when adb connection is slow. \nadb: always use adb",
    )
    aah_agent_compress = Field(
        bool,
        False,
        "aah-agent screenshot compression",
        "Use lz4 to compress screenshot data to improve screenshot speed but increase CPU usage at the same time.",
    )
    aosp_screencap_encoding = EnumField(
        ["auto", "raw", "gzip", "png"],
        "auto",
        "AOSP screencap screenshot compression",
        "Available only when transferring via adb, raw is uncompressed.",
    )
    touch_x_min = Field(
        int,
        0,
        "Touch X-axis minimum",
        "Touch X-axis minimum, used to calculate touch coordinates.",
    )
    touch_x_max = Field(
        int,
        0,
        "Touch X-axis maximum",
        "The maximum value of the touch X-axis, used to calculate the touch coordinates.",
    )
    touch_y_min = Field(
        int,
        0,
        "Touch Y-axis minimum",
        "Touch Y-axis minimum, used to calculate touch coordinates.",
    )
    touch_y_max = Field(
        int,
        0,
        "Touch Y-axis maximum",
        "The maximum value of the touch Y-axis, used to calculate the touch coordinates.",
    )
    touch_event = Field(str, "", "touch_event", "touch_event_device")


class root(Schema):
    __version__ = 5
    server = Field(Literal["US", "KR", "TW", "CN", "JP"], "US")

    @Namespace("ADB control settings")
    class device:
        adb_binary = Field(
            str,
            "",
            "ADB executable",
            """The adb command to use when you need to start the adb server. If empty, try: 1. adb in PATH; 2. ADB/{sys.platform}/adb; 3. Find Android SDK (ANDROID_SDK_ROOT and default installation directory)""",
        )
        adb_always_use_device = Field(
            str,
            "",
            "Automatically connect devices",
            "Select only this device when automatically selecting devices for connection.",
        )
        screenshot_rate_limit = Field(
            int,
            -1,
            "Screenshot rate limit",
            "Maximum number of screenshots per second, return to last screenshot if limit is exceeded. 0 means no limit, -1 means automatic limit based on time spent on last screenshot.",
        )
        wait_for_slow_network = Field(
            bool,
            True,
            "Wait for network stability before executing the operation",
            "Wait for network stability before executing the operation",
        )

        @Namespace("List of devices")
        class extra_enumerators:
            vbox_emulators = Field(
                bool,
                True,
                "Try to detect VirtualBox-based emulators (Windows)",
                "Detect running emulators via VirtualBox COM API",
            )
            bluestacks_hyperv = Field(
                bool,
                True,
                "Attempt to detect Bluestacks (Hyper-V) devices (Windows)",
                "Detect running Bluestacks via Host Compute System and Host Compute Network APIs Hyper-V instances",
            )
            append = ListField(
                str,
                ["127.0.0.1:5555", "127.0.0.1:7555"],
                "Append ADB port",
                "Append the following ADB TCP/IP port to the device list",
            )

        @Namespace("Device default settings")
        class defaults(ControllerConfig):
            pass

        adb_server = Field(
            str,
            "127.0.0.1:5037",
            "ADB server port",
            "No need to change this in most cases.",
        )

    @Namespace("combat module")
    class combat:
        @Namespace("Penguin logistics statistics")
        class penguin_stats:
            enabled = Field(
                bool,
                False,
                "Drop reporting",
                "Upload level drops to penguin logistics data (penguin-stats.io)",
            )
            endpoint = EnumField(
                ["global", "cn"],
                "global",
                "Penguin Logistics Data API endpoint",
                "global: global station; cn: China mirror",
            )
            uid = Field(
                str,
                "",
                "User ID",
                "The user ID is only used to mark your upload identity. Logging in with this ID on different devices allows the drop data to be centralized under one account, making it easy to manage uploads as well as view individual drop data. If empty, it will be created and stored in the configuration on the next upload.",
            )
            report_special_item = Field(
                bool,
                True,
                "Report special event items",
                "Report special event items whose drop rate changes with event progress",
            )

        @Namespace("Agent command error")
        class mistaken_delegation:
            settle = Field(bool, False, "Settle levels with 2 stars")
            skip = Field(
                bool,
                True,
                "Skip mistaken levels",
                "Skip subsequent times of mistaken levels",
            )

    @Namespace("Battle Plan")
    class plan:
        calc_mode = EnumField(
            ["online", "local-aog"],
            "online",
            "calc_mode",
            "online: get swipe plan from Penguin Logistics stats interface \nlocal-aog: calculate swipe plan locally, use aog recommended level optimization",
        )

    @Namespace("OCR settings (soon to be deprecated)")
    class ocr:
        backend = EnumField(
            ["auto", "tesseract", "baidu"], "auto", "default OCR backend"
        )

        @Namespace("Baidu OCR API settings")
        class baidu_api:
            enable = Field(bool, False)
            app_id = Field(str, "AMAZZ")
            app_key = Field(str, "AAAZZ")
            app_secret = Field(str, "AAAZZ")

    @Namespace("One click long grass setting")
    class grass_on_aog:
        exclude = ListField(
            str, ["solid source rock group"], "Do not brush the following materials"
        )
        prefer_activity_stage = Field(
            bool, True, "Prefer to brush levels in the activity"
        )
        no_aog_data_action = Field(
            str,
            "none",
            "action if prefer_activity_stage is enabled and aog has no data for the currently active level",
            "auto_t3: swipe minimum blue material; 1-7: swipe specified level; none: no action",
        )
        normal_action = Field(
            str,
            "auto_t3",
            "Default action if no activity",
            "auto_t3: swipe minimum blue materials; 1-7: swipe specified level; none: no action",
        )

    debug = Field(bool, False)
