console.log("Iam From JS File");
var old_present=0

function extract_jinja(jinjaData) {
  data = jinjaData.replace(/'/g, '"'); // replace single quotes with double quotes
  //console.log(data);
  const arr = JSON.parse(data);
  //console.log(arr)
  //console.log(typeof(arr))
  return arr;
}


function build_argus_card(argus_id, min_ago) {
    // This UI of Card Hearbeat Status
    // console.log("argus",argus_id, min_ago);
    let heartbeatCard = document.getElementById('heartbeatCard')
    
    let col
    if (min_ago ===  0){
      min_ago=1
    }
    if (min_ago >= 6){
      col='btn-danger'
    }else{
      col='btn-success'
    }
    new_argus_id=argus_id.slice(-2)
    let card =` 
    <a type="button" href='/retail/Truboard/heartbeat/${argus_id}' class="btn ${col} has-ripple" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="tooltip on bottom" >Device ${new_argus_id}<br> ${min_ago} min Ago <span class="ripple ripple-animate"></span></a>
    `

        // <div class="card">
    //     <div class="card-body ${col}">
    //         <div class="row align-items-center">
    //             <div class="col-12">
    //                 <h6 class="${col} text-white ">
    //                    ${min_ago} min Ago
    //                 </h6>
                 
    //             </div>
                
    //         </div>
    //     </div>
    //     <div class="card-footer bg-c-white">
    //         <div class="row align-items-center">
    //             <div class="col-12 ">
    //                 <p class="text-dark m-b-0 text-white text-nowrap font-weight-bold h6">Device ${new_argus_id}</p>
    //             </div>
               
    //         </div>
    //     </div>
    // </div>
    // console.log(card);
    const newCardElement = document.createElement('div');
    newCardElement.classList.add('m-1','p-2')
    newCardElement.innerHTML = card;

      // Append the new card element to the heartbeatCard row
  heartbeatCard.appendChild(newCardElement);
    // console.log('done')
    // heartbeatCard.innerHTML(card)
    // heartbeatCard.appendChild(card)
  // return

}

function build_contractor_card(){
  let contractorCard = document.getElementById('contractorCard');

  let cards=`
  <div class="card table-card">
                    <div class="card-header">
                        <h5>Indsao Infratech</h5>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                         <th>Total</th>
                                        <th>Attendance</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>
                                            <div class="d-inline-block align-middle">
                                            
                                                <div class="d-inline-block">
                                                    <h6 id="earlyBirdName1">Present</h6>
                                                    <!-- <p class="text-muted m-b-0">Graphics Designer</p> -->
                                                </div>
                                            </div>
                                        </td>
                                        <td><p><span id="earlyBirdValue1"> </span>&nbsp;Numerical</p></td>
                                    </tr>
                                    <tr>
                                        <td>
        
                                            <div class="d-inline-block align-middle">
                                               
                                                <div class="d-inline-block">
                                                    <h6 id="earlyBirdName2">Absent</h6>
                                                    <!-- <p class="text-muted m-b-0">Web Designer</p> -->
                                                </div>
                                            </div>
                                        </td>
                                        <td><p><span id="earlyBirdValue2"> </span>&nbsp;Numerical</p></td>
                                    </tr>
        
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
  `

const newCardElement = document.createElement('div');
    newCardElement.classList.add('col-xxl-3','col-xl-4','col-lg-6', 'col-md-7' ,'col-sm-12' ,'h-100');
    newCardElement.innerHTML = cards;
    contractorCard.appendChild(newCardElement)
}


// Defining async function
async function todayMetric(customer_name,customer_id) {
    // Storing response
    
    console.log('Running');
    // let customer_name = document.getElementById('customer_name').value;
    let new_url = $SCRIPT_ROOT + '/retail/'+ customer_name+"/todayMetric/" + customer_id;
    let response = await fetch(new_url);
  
    // Storing data in form of JSON
    let data = await response.json();
    console.log(data);
    console.log(typeof data);

    document.getElementById('todayAbsentMemeber').innerText = data.todayAbsentMemeber;
    document.getElementById('todayKnownMember').innerText = data.todayKnownMember;
    document.getElementById('todayUnknownMember').innerText = data.todayUnknownMember;
    document.getElementById('totalTeamMember').innerText = data.totalTeamMember;

   
    // todayChart(data.todayKnownMember,data.todayAbsentMemeber);
    // old_present=data.todayKnownMember;
    return data;
    
  }
  

async function allArgus(customer_name,customer_id){
  console.log('Running');
  // let customer_name = document.getElementById('customer_name').value;
  let new_url = $SCRIPT_ROOT + '/retail/'+ customer_name+"/argusStatus";
  let response = await fetch(new_url);

  // Storing data in form of JSON
  let data = await response.json();
  console.log(data);
  console.log(typeof data);
  let heartbeatCard = document.getElementById('heartbeatCard').innerText=''
  for (const argus_id in data){
    // console.log(argus_id,data[argus_id]);
    build_argus_card(argus_id,data[argus_id])
  }
}


function todayChart (present,absent){
  var xValues = ["Absent", "Present"];
  var yValues = [absent, present];
  var barColors = [
    "#ff5252",
    "#9ccc65"
  ];
  
  new Chart("TodayAttendanceSummary", {
    type: "pie",
    data: {
      labels: xValues,
      datasets: [{
        backgroundColor: barColors,
        data: yValues
      }]
    },
    options: {
    }
  });
}

async function updateEarlyBird(customer_name){
      // let customer_name = document.getElementById('customer_name').value;
      let new_url = $SCRIPT_ROOT + '/retail/'+ customer_name+"/early_bird";
      let response = await fetch(new_url);
    
      // Storing data in form of JSON
      let data = await response.json();
      console.log('Update Early Bird');
      console.log(data);
      console.log(typeof data);

     
      document.getElementById('earlyBirdName1').innerText=data.earlyBirdName1
      document.getElementById('earlyBirdName2').innerText=data.earlyBirdName2
      document.getElementById('earlyBirdValue1').innerText=data.earlyBirdValue1
      document.getElementById('earlyBirdValue2').innerText=data.earlyBirdValue2
  return true
}


async function updateThinkingFeet(customer_name){
  // let customer_name = document.getElementById('customer_name').value;
  let new_url = $SCRIPT_ROOT + '/retail/'+ customer_name+"/thinking_feet";
  let response = await fetch(new_url);

  // Storing data in form of JSON
  let data = await response.json();
  console.log('Update Early Bird');
  console.log(data);
  console.log(typeof data);

 
  document.getElementById('thinkingName1').innerText=data.thinkingName1
  document.getElementById('thinkingName2').innerText=data.thinkingName2
  document.getElementById('thinkingValue1').innerText=data.thinkingValue1
  document.getElementById('thinkingValue2').innerText=data.thinkingValue2
return true
}


async function updateMarathon(customer_name){
  // let customer_name = document.getElementById('customer_name').value;
  let new_url = $SCRIPT_ROOT + '/retail/'+ customer_name+"/marathon";
  let response = await fetch(new_url);

  // Storing data in form of JSON
  let data = await response.json();
  console.log('Update Early Bird');
  console.log(data);
  console.log(typeof data);

 
  document.getElementById('marathonName1').innerText=data.marathonName1
  document.getElementById('marathonName2').innerText=data.marathonName2
  document.getElementById('marathonValue1').innerText=data.marathonValue1
  document.getElementById('marathonValue2').innerText=data.marathonValue2
return true
}
// Calling that async function

// api url

function run_after_60_second(){
  let customer_name = document.getElementById('customer_name').innerText;
  let customer_id = document.getElementById('customer_id').innerText;
  console.log(customer_name);
  console.log('Here Iam');
  // todayMetric(customer_name,customer_id);
  allArgus(customer_name, customer_id)
}
function main(){
  let customer_name = document.getElementById('customer_name').innerText;
  let customer_id = document.getElementById('customer_id').innerText;
  console.log(customer_name);
  console.log('Here Iam');
  // Call First Time

  todayMetric(customer_name,customer_id);
  allArgus(customer_name, customer_id)

  // build_contractor_card()
  setInterval(() => run_after_60_second(), 60000);

  // updateEarlyBird(customer_name)
  // updateThinkingFeet(customer_name)
  // updateMarathon(customer_name)
}

async function fetchSubContractor(customer_name,subContractorId){
  // let customer_name = document.getElementById('customer_name').value;

  
  let new_url = $SCRIPT_ROOT +"/get_subcontractors/"+subContractorId;
  console.log('getSubCOntractor');
  let subContractorHeadingLoader=document.getElementById('subContractorHeadingLoader');
  let bodySubContractor=document.getElementById('subContractor');
  bodySubContractor.innerHTML='<br><b> Loading...   </b>'
  subContractorHeadingLoader.style.display='';
  
  let response = await fetch(new_url);
  console.log(bodySubContractor);
  bodySubContractor.innerHTML=''
  // Storing data in form of JSON
  let data = await response.json();
  console.log('Update Early Bird');
  
  console.log(data);
  console.log(typeof data);
  subContractor_data=``
  console.log(data.length);
  
  if (Object.keys(data).length === 0) {
    subContractorHeadingLoader.style.display='none';
    bodySubContractor.innerHTML='<br><b> No Sub-Contractor Found </b>'
  } else {
    subContractorHeadingLoader.style.display='none';
    for (let contractor_name in data) {
      console.log(contractor_name);
      subContractor_data = `
        <td> ${contractor_name} </td>
        <td> ${data[contractor_name][1]} </td>
        <td> ${data[contractor_name][2]} </td>
        <td> ${data[contractor_name][3]} </td>
        <td><a type="button" class="btn  btn-sm btn-outline-dark" href='/analytics' title="View Camera Analysis" >View</a></td>
      `
      const trTag = document.createElement('tr');
      //newCardElement.classList.add('col-xxl-3','col-xl-4','col-lg-6', 'col-md-7' ,'col-sm-12' ,'h-100');
      trTag.innerHTML = subContractor_data;
      bodySubContractor.appendChild(trTag)

    }
  }
  
  
 
return true
}


console.log('Welcome Dashboard JS');
document.addEventListener('DOMContentLoaded', main);


