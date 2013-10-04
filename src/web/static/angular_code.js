var app = angular.module('faceApp', [])

app.config(
    function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{_').endSymbol('_}');
    }
)


var mod = angular.module('siteManager', ['siteAjax'])

mod.directive('relationlist', function () {
    return {
        restrict: 'E',
        replace: true,
        scope: {
            placeholder: '@',
            label: '@',
            errorHeader: '@',
            addSite: '&'
        },
        templateUrl: '/static/js/sites/domain_form.html',
        controller: function ($scope, $http) {


        }
    };
})

