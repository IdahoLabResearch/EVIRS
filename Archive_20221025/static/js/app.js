function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

function SetCheckOnButton(id)
{
  document.getElementById(id).checked = true;
}

function updateVinSubModelList(data, defaultOptionVal, defaultOptionText)
{
      var str='<option value="'+defaultOptionVal+'">'+defaultOptionText+'</option>';
      let li = JSON.parse(data).submodellist;
      for (let i=0;i < li.length; i++)
      {
        str += '<option value="'+li[i]+'">'+li[i]+'</option>';
      }
      return str;
}

function updateMakeList(data, defaultOptionVal, defaultOptionText) {
  var str='<option value="'+defaultOptionVal+'">'+defaultOptionText+'</option>';
  let li = JSON.parse(data).makelist;
  for (let i=0;i < li.length; i++)
  {
    str += '<option value="'+li[i]+'">'+li[i]+'</option>';
  }
  return str;
}

function updateModelList(data, defaultOptionVal, defaultOptionText) {
  var str='<option value="'+defaultOptionVal+'">'+defaultOptionText+'</option>';
  let li = JSON.parse(data).modellist;
  for (let i=0;i < li.length; i++)
  {
    str += '<option value="'+li[i]+'">'+li[i]+'</option>';
  }
  return str;
}

function updateYearList(data, defaultOptionVal, defaultOptionText) {
  var str='<option value="'+defaultOptionVal+'">'+defaultOptionText+'</option>';
  let li = JSON.parse(data).yearlist;
  for (let i=0;i < li.length; i++)
  {
    str += '<option value="'+li[i]+'">'+li[i]+'</option>';
  }
  return str;
}

function updateSubmodelList(data, defaultOptionVal, defaultOptionText) {
  var str='<option value="'+defaultOptionVal+'">'+defaultOptionText+'</option>';
  let li = JSON.parse(data).submodellist;
  for (let i=0;i < li.length; i++)
  {
    if (li[i] == null) continue;
    str += '<option value="'+li[i]+'">'+li[i]+'</option>';
  }
  return str;
}

function showErrMsg(id, msg)
{
  msglabel = document.getElementById(id);
  msglabel.innerHTML = msg;
  msglabel.hidden = false;
}

function hideErrMsg(id)
{
  msglabel = document.getElementById(id);
  msglabel.hidden = true;
}

function checkVin() {
  let r = {
    url: '/check_vin',
    type: 'POST',
    data: JSON.stringify({'vin' : $(this).val()}),
    datatype: 'json',
    success: function(data) {
      hideErrMsg("vin_errmsg");
      str = updateVinSubModelList(data, "All", "All (not sure)");
      document.getElementById("vinsubmodellist").innerHTML = str;
    },
    error: function(request, error) {
      console.log(request);
      console.log(error);
      showErrMsg("vin_errmsg", "Bad VIN. Try again.");
    }
  };

  $.ajax(r);
}

function getMakeList() {
  let r = {
    url: '/get_makes',
    type: 'GET',
    //data: JSON.stringify({'vin' : $(this).val()}),
    datatype: 'json',
    success: function(data) {
      str = updateMakeList(data, "-", "-Select Make-");
      document.getElementById("makelist").innerHTML = str;
    },
    error: function(request, error) {
      showErrMsg("makes_errmsg", "Error getting makes");
    }
  };
  $.ajax(r);
}

function getModelList() {
  let r = {
    url: '/get_models',
    type: 'POST',
    data: JSON.stringify({'make' : $(this).val()}),
    datatype: 'json',
    success: function(data) {
      str = updateModelList(data, "-", "-Select Model-");
      document.getElementById("modellist").innerHTML = str;
    },
    error: function(request, error) {
      alert(error);
    }
  };
  $.ajax(r);
}

function getYearList() {
  let make = document.getElementById('makelist').value;
  let r = {
    url: "/get_years",
    type: 'POST',
    data: JSON.stringify({'model' : $(this).val(), 'make' : make}),
    datatype: 'json',
    success: function(data) {
      str = updateYearList(data, "-", "-Select Year-");
      document.getElementById('yearlist').innerHTML = str;
    },
    error: function(request, error) {
      alert(error);
    }
  };
  $.ajax(r);
}

function getSubmodelList() {
  let make = document.getElementById('makelist').value;
  let model = document.getElementById('modellist').value;
  let r = {
    url: "/get_submodels",
    type: 'POST',
    data: JSON.stringify({'year' : $(this).val(), 'make' : make, 'model' : model}),
    datatype: 'json',
    success: function(data) {
      str = updateSubmodelList(data, "All", "All (not sure)");
      document.getElementById('submodellist').innerHTML = str;
    },
    error: function(request, error) {
      alert(error);
    }
  };
  $.ajax(r);
}

function enterKeySubmit(event){
  if (event.keyCode == 13) {
    document.getElementById("formSubmitBtn").click()
  }
}

// function showImage(imageID, image)
// {
//   document.getElementById("carfigure").src = "data:image/jpg;base64," + image;
// }

// open starting tab
$(document).ready(function(){
  document.getElementById("defaultOpen").click();
  getMakeList();
  showSlides(1);
});

$(document).ready(function(){
  $("#vin").on("change", checkVin);
  $("#makelist").on("change", getModelList);
  $("#modellist").on("change", getYearList);
  $("#yearlist").on("change", getSubmodelList);
  $('#myform').validate({
      submitHandler: function(form) {
        
      }
  })

  $("form").submit(function (event) {
    // var formData = {
    //   vin: $("#vin").val(),
    //   submodellist: $("vinsubmodellist").val(),
    // };
    var formData = JSON.stringify(
      {'vin'         : $("#vin").val(), 
      'submodellist': $("#vinsubmodellist").val(),
      'vehicle': $("input[name='vehicle']:checked").val()
    });

    var data = "";


    $.ajax({
      type: "POST",
      url: "/validate_form",
      data: formData,
      datatype: "json",
    }).done(function (data) {
      data = JSON.parse(data);
      // console.log(data);

      if(data.status != 'ok') {
        document.getElementById('vin_errmsg').innerHTML = "Please enter VIN or Make, Model, and Year below";
        document.getElementById('vin_errmsg').hidden = false;

        // $("#vin_errmsg").addclass("has-error");
        // $("#vin_errmsg").append(
        //   '<div class="help-block">' + data.errmsg + "</div>"
        // );
      }
      else {
        $.ajax({
          type: "POST",
          url: "/",
          data: formData,
          datatype: "json",
        }).done(function (data) {
          // console.log(data);
          document.write(data);
    
        })
      }
    })
  })
  // event.preventDefault();
});
