 $(document).ready(function(){
  $("#searchCab").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myCabs tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
    $("#otherCabs tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});



