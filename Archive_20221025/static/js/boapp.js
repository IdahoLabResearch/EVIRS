// function calcData(curMiles, ids, rngs){
//   for(i=0;i<ids.length;i++) {
//     if (curMiles == "") {
//       socPct = "";
//     }
//     else {
//       if (curMiles > rngs[i]){
//         socPct = "<span style='font-size:small;color:red;'>?: <i>miles>range</i></span>";
//       }
//       else {
//         let s = 100 *curMiles / rngs[i];
//         socPct = s.toFixed(1) + "%";
//       }
//     }
//     sp = document.getElementById("socPct"+ids[i]);
//     sp.innerHTML = socPct;
//   }
// }

function calcData(curMiles, ids, rngs, kWh, maxvolt, minvolt){
    for(i=0;i<ids.length;i++) {
      if (curMiles == "") {
        socPct = "";
      }
      else {
        if (curMiles > rngs[i]){
          socPct = "<span style='font-size:small;color:red;'>?: <i>miles>range</i></span>";
        }
        else {
          let s = 100 *curMiles /  rngs[i];
          socPct = s.toFixed(1) + "%";

          s = curMiles / rngs[i] * kWh[i] ;
          kwhStranded = s.toFixed(2);

          s = minvolt[i] + (maxvolt[i] - minvolt[i]) * curMiles /  rngs[i] ;
          curPackVoltage = s.toFixed(2);


        }
      }
      sp = document.getElementById("socPct"+ids[i]);
      sp.innerHTML = socPct;

      sp = document.getElementById("kwhStranded"+ids[i]);
      sp.innerHTML = kwhStranded;

      sp = document.getElementById("curPackVoltage"+ids[i]);
      sp.innerHTML = curPackVoltage;


    }
  }