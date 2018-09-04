# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import types
import octoprint.plugin

def _updateProgressDataCallback(self):
    if self._comm is None:
            progress = None
            filepos = None
            printTime = None
            cleanedPrintTime = None
            time_progress = None
    else:
            progress = self._comm.getPrintProgress()
            time_progress = 0.0
            filepos = self._comm.getPrintFilepos()
            printTime = self._comm.getPrintTime()
            cleanedPrintTime = self._comm.getCleanedPrintTime()

    printTimeLeft = printTimeLeftOrigin = None
    estimator = self._estimator
    if progress is not None:
            if progress == 0:
                    printTimeLeft = None
                    printTimeLeftOrigin = None
                    time_progress = 0.0
            elif progress == 1.0:
                    printTimeLeft = 0
                    printTimeLeftOrigin = None
                    time_progress = 1.0
            elif estimator is not None:
                    statisticalTotalPrintTime = None
                    statisticalTotalPrintTimeType = None
                    with self._selectedFileMutex:
                            if self._selectedFile and "estimatedPrintTime" in self._selectedFile \
                                            and self._selectedFile["estimatedPrintTime"]:
                                    statisticalTotalPrintTime = self._selectedFile["estimatedPrintTime"]
                                    statisticalTotalPrintTimeType = self._selectedFile.get("estimatedPrintTimeType", None)

                    printTimeLeft, printTimeLeftOrigin = estimator.estimate(progress,
                                                                            printTime,
                                                                            cleanedPrintTime,
                                                                            statisticalTotalPrintTime,
                                                                            statisticalTotalPrintTimeType)

                    if printTimeLeft is not None:
                        time_progress = printTime / (printTime + printTimeLeft)

            time_progress_int = int(time_progress * 1000)
            if self._lastProgressReport != time_progress_int:
                    self._lastProgressReport = time_progress_int
                    self._reportPrintProgressToPlugins(time_progress_int / 10)

    return self._dict(
                        completion=time_progress * 100 if time_progress is not None else None,
                        file_completion=progress * 100 if progress is not None else None,
                        filepos=filepos,
                        printTime=int(printTime) if printTime is not None else None,
                        printTimeLeft=int(printTimeLeft) if printTimeLeft is not None else None,
                        printTimeLeftOrigin=printTimeLeftOrigin)


class ProgressBasedOnTimePlugin(octoprint.plugin.SettingsPlugin,
                                octoprint.plugin.AssetPlugin,
                                octoprint.plugin.TemplatePlugin,
                                octoprint.plugin.StartupPlugin):

    ##~~ SettingsPlugin mixin

    def on_startup(self, host, port):
        self._printer._stateMonitor._on_get_progress = types.MethodType(_updateProgressDataCallback, self._printer)

    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/ProgressBasedOnTime.js"],
            css=["css/ProgressBasedOnTime.css"],
            less=["less/ProgressBasedOnTime.less"]
        )

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            ProgressBasedOnTime=dict(
                displayName="ProgressBasedOnTime Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="celogeek",
                repo="OctoPrint-ProgressBasedOnTime",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/celogeek/OctoPrint-ProgressBasedOnTime/archive/{target_version}.zip"
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "ProgressBasedOntime Plugin"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = ProgressBasedOnTimePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
