function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  // $('[name="tabcontent"]').attr("style", "display:none");
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

function SetVINEntryCheck() {
  document.getElementById("vinbtn").checked = true;
}

function SetCheckOnButton(id) {
  document.getElementById(id).checked = true;
}

function showErrMsg(id, msg) {
  msglabel = document.getElementById(id);
  msglabel.innerHTML = msg;
  msglabel.style.backgroundColor = "#FFFF00"
}

function hideErrMsg(id) {
  msglabel = document.getElementById(id);
  msglabel.innerHTML = "&nbsp;"
  msglabel.style.backgroundColor = ""
}

function updateVinSubModelList(submodels, defaultOptionVal, defaultOptionText) {
      var str='<option value="'+defaultOptionVal+'">'+defaultOptionText+'</option>';
      for (let i=0;i < submodels.length; i++)
      {
        str += '<option value="'+submodels[i]+'">'+submodels[i]+'</option>';
      }
      return str;
}

function checkVin() {
  let r = {
    url: '/check_vin',
    type: 'POST',
    data: JSON.stringify({'vin' : $(this).val()}),
    datatype: 'json',
    success: function(data) {
      data = JSON.parse(data);
      submodels = data.submodellist;
      hideErrMsg("vin_errmsg");
      if (data.status != "ok") {
        showErrMsg("vin_errmsg", data.message);
      }
      else {
        if (data.numsubmodels == 1){
          str = `<option value="${submodels[0]}">${submodels[0]}</option>`;
        }
        else {
          str = updateVinSubModelList(submodels, "All", "All (not sure)");
        }
        $("#vinsubmodellist").html(str);
        // getYearList();
      }
    },
    error: function(request, error) {
      console.log(request);
      console.log(error);
      showErrMsg("vin_errmsg", "Error occured using VIN");
    }
  };

  $.ajax(r);
}

function updateMakeList(makes, defaultOptionVal, defaultOptionText) {
  var str='<option value="'+defaultOptionVal+'">'+defaultOptionText+'</option>';
  for (let i=0;i < makes.length; i++)
  {
    str += '<option value="'+makes[i]+'">'+makes[i]+'</option>';
  }
  return str;
}

function getMakeList() {
  let r = {
    url: '/get_makes',
    type: 'GET',
    datatype: 'json',
    success: function(data) {
      data = JSON.parse(data);
      makes = data.makelist;
      str = updateMakeList(makes, "-", "-Select Make-");
      document.getElementById("makelist").innerHTML = str;
    },
    error: function(request, error) {
      showErrMsg("makes_errmsg", "Error getting makes");
    }
  };
  $.ajax(r);
}

function updateModelList(models, defaultOptionVal, defaultOptionText) {
  var str='<option value="'+defaultOptionVal+'">'+defaultOptionText+'</option>';
  for (let i=0;i < models.length; i++)
  {
    str += '<option value="'+models[i]+'">'+models[i]+'</option>';
  }
  return str;
}

function getModelList() {
  let r = {
    url: '/get_models',
    type: 'POST',
    data: JSON.stringify({'make' : $(this).val()}),
    datatype: 'json',
    success: function(data) {
      data = JSON.parse(data);
      models = data.modellist;

      if (data.nummodels == 1){
        str = `<option value="${models[0]}">${models[0]}</option>`;
      }
      else {
        str = updateModelList(models, "-", "-Select Model-");
      }
      $("#modellist").html(str);
      getYearList();
    },
    error: function(request, error) {
      alert(error);
    }
  };
  $.ajax(r);
}

function updateYearList(years, defaultOptionVal, defaultOptionText) {
  var str='<option value="'+defaultOptionVal+'">'+defaultOptionText+'</option>';
  for (let i=0;i < years.length; i++)
  {
    str += '<option value="'+years[i]+'">'+years[i]+'</option>';
  }
  return str;
}

function getYearList() {
  let make = document.getElementById('makelist').value;
  let model = document.getElementById('modellist').value;
  let r = {
    url: "/get_years",
    type: 'POST',
    data: JSON.stringify({'model' : model, 'make' : make}),
    datatype: 'json',
    success: function(data) {
      data = JSON.parse(data);
      years = data.yearlist;
      if (data.numyears == 1){
        str = `<option value="${years[0]}">${years[0]}</option>`;
      }
      else {
        str = updateYearList(years, "All", "All (not sure)");
      }
      $("#yearlist").html(str);
      getSubmodelList();
    },
    error: function(request, error) {
      alert(error);
    }
  };
  $.ajax(r);
}

function updateSubmodelList(submodels, defaultOptionVal, defaultOptionText) {
  var str='<option value="'+defaultOptionVal+'">'+defaultOptionText+'</option>';
  for (let i=0;i < submodels.length; i++)
  {
    if (submodels[i] == null) continue;
    str += '<option value="'+submodels[i]+'">'+submodels[i]+'</option>';
  }
  return str;
}

function getSubmodelList() {
  let make = document.getElementById('makelist').value;
  let model = document.getElementById('modellist').value;
  let year = document.getElementById('yearlist').value;
  let r = {
    url: "/get_submodels",
    type: 'POST',
    data: JSON.stringify({'year' : year, 'make' : make, 'model' : model}),
    datatype: 'json',
    success: function(data) {
      data = JSON.parse(data);
      submodels = data.submodellist;
      str = updateSubmodelList(submodels, "All", "All (not sure)");
      document.getElementById('submodellist').innerHTML = str;
      if (data.numsubmodels == 1){
        document.getElementById("submodellist").value = submodels[0];
      }
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

function windowresized(event) {
  c = document.getElementById("s4-bodyContainer");
  w = document.documentElement.clientWidth;
  if (w<1300){
    c.style.width = w-20;
  }
    else {
    c.style.width = 1400;
  }
}

function calcDischargeTable(ids, submodel, gotYearRange, years, kwh, amps) {
  disPct = document.getElementById("dischargePct").value;
  disTime = document.getElementById("dischargeTime").value;
  // tblDisPct = document.getElementById("tblDisPct");
  // tblDisTime = document.getElementById("tblDisTime");

  $("#tblDisPct").html(`${disPct}%`);
  // tblDisPct.innerHTML = disPct + "%";
  
  $("#tblDisTime").html(disTime + (disTime == 1 ? " hour" : " hours"));
  // tblDisTime.innerHTML = disTime + (disTime == 1 ? " hour" : " hours");
  disPct = 0.01 * disPct;
  
  for(i=0;i<ids.length;i++) {
    $(`#disSubmodel${ids[i]}`).html(submodel[i]);
    if (gotYearRange) {
      $(`#disYears${ids[i]}`).html(`averaged for years ${years[i]}`);
    }
    s = (kwh[i] * disPct / disTime).toFixed(1);
    $(`#diskWh${ids[i]}`).html(s);

    s = (amps[i] * disPct / disTime).toFixed(1);
    $(`#disAmps${ids[i]}`).html(s);

  }
}

// function updateUserDischargeEntry() {
//   // n = document.getElementById('dischargeTime').value;
//   n = $("#dischargeTime").val();
//   n = Number(n).toFixed(1);
//   // document.getElementById('dischargeHours').innerHTML= n;
//   $("#dischargeHours").html(n);
// }

function showGuide(doc, frameid, dialogid) {
  $(`#${frameid}`).attr("src", doc);
  document.getElementById(dialogid).showModal();
}

function togglePackVoltElements() {
  calcVoltChk = document.getElementById("pg1CalcPackVolts");

  if (calcVoltChk.checked) {
    calcdisplay = "inherit"
    enterdisplay = "none"
    $("#curmiles").prop("disabled", false);
    $("#miles").prop("hidden", false);
    $("#packVoltageLabel").html("Estimated Pack Voltage");
    $("#packVoltageTooltip").html("Estimated Pack Voltage");
    $("#socTooltip").html("Estimate based on remaining miles");
    $("#strandedkwhTooltip").html("Estimate based on remaining miles");
  }
  else {
    calcdisplay = "none"
    enterdisplay = "inherit"
    $("#curmiles").prop("disabled", true);
    $("#miles").prop("hidden", true);
    $("#packVoltageLabel").html("Measured Pack Voltage");
    $("#packVoltageTooltip").html("<b>Enter Voltage measurement from vehicle</b>");
    $("#socTooltip").html("Based on pack voltage measurement");
    $("#strandedkwhTooltip").html("Based on pack voltage measurement");
    $("#curmiles").val("");
    $("#miles").text("");
  }
  clearCalcData();

  $('[name="calcVoltObj"]').attr("style", `display:${calcdisplay}`);
  $('[name="enterVoltObj"]').attr("style", `display:${enterdisplay}`);
  $('[name="enterVoltObj"]').val("");
}

function setupZoombox() {
  // (A) GET LIGHTBOX & ALL .ZOOMD IMAGES
  let all = document.getElementsByClassName("zoomD"),
  lightbox = document.getElementById("lightbox");
  // (B) CLICK TO SHOW IMAGE IN LIGHTBOX
  // * SIMPLY CLONE INTO LIGHTBOX & SHOW
  if (all.length>0) { 
    for (let i of all) {
      i.onclick = () => {
        let clone = i.cloneNode();
        clone.className = "";
        clone.id = "";
        clone.style = "weight:100%; height:100%; cursor:pointer;";
        lightbox.innerHTML = "";
        lightbox.appendChild(clone);
        lightbox.className = "show";
      };
    }
  }
  // (C) CLICK TO CLOSE LIGHTBOX
  lightbox.onclick = () => {
    lightbox.className = "";
  };
}

function manageGuidelines() {
  var guidesmodal = document.querySelector("#guides-dialog")
  guidebuttons = document.getElementsByClassName("guidebutton")
        for (btn of guidebuttons) {
            btn.addEventListener("click", () => {guidesmodal.showModal();})
        }
  // document.querySelector(".button-container button").addEventListener("click", () => {
  //   modal.showModal();
  // });

  var closeBtns = document.getElementsByClassName("guides-dialog-close");

  for (btn of closeBtns) {
    btn.addEventListener("click", () => {
      guidesmodal.close();
    })
  }
}

$(document).ready(function(){
  window.onresize = windowresized;
  setupZoombox();
  document.getElementById("defaultPage").click();
  getMakeList();

  $("#vinentrybox").on("input", SetVINEntryCheck);
  $("#vinentrybox").on("change", checkVin);
  $("#makelist").on("change", getModelList);
  $("#modellist").on("change", getYearList);
  $("#yearlist").on("change", getSubmodelList);
  // Event for when new vehicle is selected
  $("#formSubmitBtn").click(function(event){
    event.preventDefault();
    let r = {
      url: $("#myform")[0].action,
      type: $("#myform")[0].method,
      data: JSON.stringify($("#myform").serialize()),
      success: function(response) {
        hideErrMsg("vin_errmsg");
        hideErrMsg("mmy_errmsg");
        if (response["status"] == "vin_error") {
          showErrMsg("vin_errmsg", response["message"]);
        }
        if (response["status"] == "mmy_error") {
          showErrMsg("mmy_errmsg", response["message"]);
        }
        else {
          // Refresh content
          $('#Page1Span').html(response['page1']);
          $('#Page2Span').html(response['page2']);
          $('#Page3Span').html(response['page3']);
          $('#Page4Span').html(response['page4']);
          $('#EducationSpan').html(response['education']);
          enterVoltElements = document.getElementsByName("enterVoltObj")
          enterVoltElements.forEach(element => {
            element.style.display = "none";
          });
          setupZoombox();
          document.getElementById("defaultPage").click();
        }
      }
    }
    $.ajax(r);
  });
});

function thumbClick(img, caption)
{
  currentImage = document.getElementById("current-image");
  currentCaption = document.getElementById("current-caption");
  currentImage.src = img;
  currentImage.alt = caption;
  currentCaption.innerHTML = caption
}
