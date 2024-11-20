// function packVoltageCalcData(ids, kwhrated, maxvolt, minvolt) {
//   for(i=0;i<ids.length;i++) {
//     volts = document.getElementById("enteredPackVoltage"+ids[i]).value;
//     if (volts == "" || volts < minvolt[i]) {
//       socPct = "";
//       strandedkwh = "";
//     }
//     else {
//       let soc = (volts - minvolt[i]) / (maxvolt[i] - minvolt[i]);
//       socPct = (100 * soc).toFixed(2) + "%";
//       strandedkwh = (kwhrated[i] * soc).toFixed(2);
//     }
//     $(`#socPct${ids[i]}`).html(socPct);
//     $(`#disSOC${ids[i]}`).html(socPct);
//     $(`#kwhStranded${ids[i]}`).html(strandedkwh);
//   }
// }

function packVoltageCalcData(ids, chem, kwhrated, maxvolt, minvolt) {
  for(i=0;i<ids.length;i++) {
    volts = document.getElementById("enteredPackVoltage"+ids[i]).value;
    if (volts == "" || volts < minvolt[i] || volts > maxvolt[i]) {
      socPct = `<font style="font-size:small;font-weight:normal;font-style:italic">outside normal range<br>(volts: ${minvolt[i]} - ${maxvolt[i]})</font>`;
      strandedkwh = "";
    }
    else {
      if (chem[i]=='grnca'){
          pervolt = 2.7 + (volts - minvolt[i]) / (maxvolt[i] - minvolt[i]) * (4.18 - 2.7);
          if (pervolt <= 3.32) {
            soc = (pervolt - 2.7) / (3.32 - 2.7) * 5.13;
          }
          else {
            soc = 5.13 + (pervolt - 3.32) / (4.18 - 3.32) * ( 100 - 5.13);
          }
        }
      // default to linear calculation if a non-linear mode was not found
      else {
        soc = (volts - minvolt[i]) / (maxvolt[i] - minvolt[i]) * 100;
      }    
      socPct = soc.toFixed(2) + "%";
      strandedkwh = (kwhrated[i] * soc/100).toFixed(2);
    }
    $(`#socPct${ids[i]}`).html(socPct);
    $(`#disSOC${ids[i]}`).html(socPct);
    $(`#kwhStranded${ids[i]}`).html(strandedkwh);
  }
}

function clearCalcData() {
  $("[name=socPctObj").html("");
  $("[name=kwhStrandedObj").html("");
  $("[name=calcVoltObj").html("");
  $("[name=enterVoltObj").html("");
}

function remainingMilesCalcData(curMiles, ids, rngs, kWh, chem, maxvolt, minvolt){
    errLabel = document.getElementById("miles")
    errLabel.hidden = true;
    errMsg = "";
    for(i=0;i<ids.length;i++) {
      hoverMsg = `based on ${rngs[i]} mile range`;
      outOfRange=false
      rangeErrVal = "";
      if (curMiles == "") outOfRange = true;
      if (curMiles != "") {
        if (curMiles.match(/^[0-9]+$/) == null) {
          rangeErrVal = "";
          outOfRange = true;
          if (errMsg == "") {
            errMsg = 'not a valid value';
          }
        }
        else if (curMiles > rngs[i]){
          hoverMsg = `miles entered are greater than the vehicle's ${rngs[i]} mile range`;
          rangeErrVal = "<span style='font-size:small;color:red;'><i> -- </i></span>";
          outOfRange = true;
          if (errMsg == "") {
            errMsg = `value is greater than a vehicle's range`;
          }
        }
        else {
          let socPercent = 100 *curMiles /  rngs[i];
          socPct = socPercent.toFixed(2) + "%";

          s = curMiles / rngs[i] * kWh[i];
          kwhStranded = s.toFixed(2);

          if (chem[i]=='grnca'){
          // the non-linear calculation for grnca goes here (for now we just use the linear equation until Bo provide further instructions)
            midvolt = minvolt[i] + (maxvolt[i] - minvolt[i]) * (3.32 - 2.7) /  (4.18 - 2.7);
          
            if (socPercent <= 5.13){
              s = minvolt[i] + (midvolt - minvolt[i]) * ( socPercent / 5.13);
            }
            else {
              s = midvolt + (maxvolt[i] - midvolt) * ( (socPercent - 5.13) / (100-5.13));
            }
          }
          // this is the linear calculation - we default to it if a non-linear mode was not found
          else {
            s = minvolt[i] + (maxvolt[i] - minvolt[i]) * curMiles /  rngs[i];
          }
          curPackVoltage = s.toFixed(2);
        }
      }
      if (errMsg != "") {
        errLabel.innerHTML = errMsg;
        errLabel.hidden = false;          
      }
      $(`#socPct${ids[i]}`).prop("title", hoverMsg)
      $(`#socPct${ids[i]}`).html(outOfRange ? rangeErrVal : socPct)

      $(`#disSOC${ids[i]}`).html(outOfRange ? rangeErrVal : socPct)

      $(`#kwhStranded${ids[i]}`).prop("title", hoverMsg)
      $(`#kwhStranded${ids[i]}`).html(outOfRange ? rangeErrVal : kwhStranded)

      $(`#curPackVoltage${ids[i]}`).prop("title", hoverMsg)
      $(`#curPackVoltage${ids[i]}`).html(outOfRange ? rangeErrVal : curPackVoltage)
    }
 }