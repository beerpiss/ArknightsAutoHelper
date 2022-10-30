from automator import AddonBase, cli_command


class RecruitAddon(AddonBase):
    def recruit(self):
        import imgreco.recruit
        from . import recruit_calc

        self.logger.info("Identifying recruitment tags")
        tags = imgreco.recruit.get_recruit_tags(self.screenshot())
        self.logger.info("Tags found: %s", " ".join(tags))
        if len(tags) != 5:
            self.logger.warning(
                "Not enough tags (only %d out of 5) were identified.", len(tags)
            )
        result = recruit_calc.calculate(tags)
        self.logger.debug("计算结果：%s", repr(result))
        return result

    @cli_command("recruit")
    def cli_recruit(self, argv):
        """
        recruit [tags ...]
        Automatically calculate recruitment tags
        """
        from . import recruit_calc

        if 2 <= len(argv) <= 6:
            tags = argv[1:]
            result = recruit_calc.calculate(tags)
        elif len(argv) == 1:
            with self.helper.frontend.context:
                result = self.recruit()
        else:
            print("Too many tags")
            return 1

        colors = [
            "\033[36m",
            "\033[90m",
            "\033[37m",
            "\033[32m",
            "\033[93m",
            "\033[91m",
        ]
        reset = "\033[39m"
        for tags, operators, rank in result:
            taglist = ",".join(tags)
            if rank >= 1:
                taglist = "\033[96m" + taglist + "\033[39m"
            print(
                "%s: %s"
                % (taglist, " ".join(colors[op[1]] + op[0] + reset for op in operators))
            )
