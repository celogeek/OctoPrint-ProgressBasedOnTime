/*
 * View model for OctoPrint-ProgressBasedOnTime
 *
 * Author: Celogeek
 * License: AGPLv3
 */
$(function() {
    function ProgressBasedOnTimeViewModel(parameters) {
        var self = this;
        self.printerState = parameters[0]

        // restore original data process to ensure JS interface can handle it properly.
        self.onAfterBinding = function() {
            const processProgressData = self.printerState._processProgressData.bind(self.printerState)
            self.printerState._processProgressData = function(data) {
                if (data.file_completion) {
                    data.completion = data.file_completion
                }
                processProgressData(data)
            }
        }
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: ProgressBasedOnTimeViewModel,
        dependencies: [ "printerStateViewModel" ],
        elements: [ ]
    });
});
