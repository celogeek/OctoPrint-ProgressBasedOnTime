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
import logging


def progressCallBack(origCallback, plugin):
    def callback(self):
        result = dict(origCallback())

        file_completion = result['completion']
        time_completion = None
        if file_completion is not None:
            if result['printTimeLeft'] < 0:
                time_completion = 100.0
            else:
                time_completion = float(result['printTime']) * 100.00 / float(result['printTime'] + result['printTimeLeft'])

        result.update(
            completion=time_completion,
            file_completion=file_completion,
            time_completion=time_completion,
        )

        return self._dict(result)

    return callback


class ProgressBasedOnTimePlugin(octoprint.plugin.SettingsPlugin,
                                octoprint.plugin.AssetPlugin,
                                octoprint.plugin.TemplatePlugin,
                                octoprint.plugin.StartupPlugin):

    ##~~ SettingsPlugin mixin
    def on_startup(self, host, port):
        self._printer._stateMonitor._on_get_progress = types.MethodType(
            progressCallBack(self._printer._stateMonitor._on_get_progress, self)
        , self._printer)

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
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = ProgressBasedOnTimePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }


