angular.module('myApp', [])
    .controller('HomeCtrl', function($scope, $http) {

$scope.info = {};

$scope.showAdd = true;

$scope.showlist = function(){
  $http({
    method: 'GET',
    url: '/api/wenxue',
  }).then(function(response) {
    $scope.news_item = response.data;
    console.log('news items',$scope.news_item);
  }, function(error) {
    console.log(error);
  });
}


$scope.addMachine = function(){
  $http({
    method: 'POST',
    url: '/addMachine',
    data: {info:$scope.info}
  }).then(function(response) {
    $scope.showlist();
    $('#addPopUp').modal('hide')
    $scope.info = {}
  }, function(error) {
    console.log(error);
  });
}


$scope.editNews = function(id){
  $scope.info.id = id;
  $scope.showAdd = false;
  $http({
    method: 'GET',
    url: '/api/wenxue/' +$scope.info.id
  }).then(function(response) {
    console.log(response);
    $scope.info = response.data;
    $('#addPopUp').modal('show')
  }, function(error) {
    console.log(error);
  });
}

$scope.updateMachine = function(id){
  $http({
    method: 'POST',
    url: '/updateMachine',
    data: {info:$scope.info}
  }).then(function(response) {
    console.log(response.data);
    $scope.showlist();
    $('#addPopUp').modal('hide')
  }, function(error) {
    console.log(error);
  });
}


$scope.showAddPopUp = function(){
  $scope.showAdd = true;
  $scope.info = {};
  $('#addPopUp').modal('show')
}

$scope.showRunPopUp = function(id){
  $scope.info.id = id;
  $scope.run = {};
  $http({
    method: 'POST',
    url: '/getMachine',
    data: {id:$scope.info.id}
  }).then(function(response) {
    console.log(response);
    $scope.run = response.data;
    $scope.run.isRoot = false;
    $('#runPopUp').modal('show');
  }, function(error) {
    console.log(error);
  });


}

$scope.confirmDelete = function(id, title){
  $scope.deleteNewsId = id;
  $scope.deleteTitle = title;
  $('#deleteConfirm').modal('show');
}

$scope.deleteNews = function(){
  $http({
    method: 'DELETE',
    url: '/api/wenxue/' +$scope.deleteNewsId
  }).then(function(response) {
    console.log(response.data);
    $scope.deleteNewsId = '';
    $scope.showlist();
    $('#deleteConfirm').modal('hide')
  }, function(error) {
    console.log(error);
  });
}


$scope.executeCommand = function(){


  console.log($scope.run);

  $http({
    method: 'POST',
    url: '/execute',
    data: {info:$scope.run}
  }).then(function(response) {
    console.log(response);
    $scope.run.response = response.data.message;
  }, function(error) {
    console.log(error);
  });
}

$scope.showlist();
    })
