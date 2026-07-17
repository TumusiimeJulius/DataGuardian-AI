import { useEffect, useState } from "react";
import * as WebSocketHook from "react-use-websocket";

import api from "../services/api";
import Layout from "../components/Layout";

import {
  FaDatabase,
  FaHeartbeat,
  FaTools,
  FaExclamationTriangle,
  FaWifi,
  FaPlug,
  FaLightbulb,
  FaDownload,
  FaRobot
} from "react-icons/fa";




// react-use-websocket Vite Fix
let useWebSocket: any = WebSocketHook;
if (useWebSocket && typeof useWebSocket !== "function") {
  if (typeof useWebSocket.default === "function") {
    useWebSocket = useWebSocket.default;
  } else if (useWebSocket.default && typeof useWebSocket.default.default === "function") {
    useWebSocket = useWebSocket.default.default;
  } else if (typeof useWebSocket.useWebSocket === "function") {
    useWebSocket = useWebSocket.useWebSocket;
  }
}





export default function Dashboard(){


const [data,setData]=useState<any>(null);

const [cleanFile,setCleanFile]=useState("");






// ===============================
// WEBSOCKET
// ===============================


const {

lastJsonMessage,

readyState

}=useWebSocket(

"ws://dataguardianai.onrender.com/ws/dashboard",

{

shouldReconnect:()=>true,

reconnectAttempts:20,

reconnectInterval:3000

}

);








// ===============================
// LOAD DASHBOARD
// ===============================


useEffect(()=>{


async function load(){


try{


const response =
await api.get(
"/dashboard/overview"
);



setData(response.data);



// get cleaned dataset

if(response.data.repair){

setCleanFile(

response.data.repair.clean_file

);

}



}

catch(error){

console.error(
"Dashboard Error",
error
);

}



}



load();


},[]);










// ===============================
// LIVE UPDATE
// ===============================


useEffect(()=>{


if(!lastJsonMessage)

return;



setData((old:any)=>({


...old,


realtime:lastJsonMessage


}));


},[lastJsonMessage]);







if(!data){


return(

<Layout>

<h2 style={{color:"white"}}>

Loading DataGuardian AI...

</h2>

</Layout>

);


}







const realtime =
data.realtime || {};


const analysis =
data.analysis || {};






return(


<Layout>


<div style={{
color:"white"
}}>





{/* HEADER */}


<div

style={{

display:"flex",

justifyContent:"space-between",

alignItems:"center",

marginBottom:30

}}

>


<h1>

🚀 DataGuardian AI Operations Center

</h1>





<div

style={{

background:"#1e293b",

padding:"12px 20px",

borderRadius:12

}}

>


{

readyState===1 ?


<span style={{
color:"#22c55e"
}}>

<FaWifi/>

 Connected

</span>


:

<span style={{
color:"orange"
}}>

<FaPlug/>

 Connecting

</span>


}


</div>


</div>









{/* STATISTICS */}



<div

style={{

display:"grid",

gridTemplateColumns:

"repeat(auto-fit,minmax(220px,1fr))",

gap:20

}}

>


<Card

title="Quality Score"

value={

analysis.quality_score ?

`${analysis.quality_score}%`

:

"Waiting"

}

icon={<FaHeartbeat/>}

/>




<Card

title="Missing Values"

value={

analysis.missing_values ?? 0

}

icon={<FaDatabase/>}

/>





<Card

title="Duplicates"

value={

analysis.duplicates ?? 0

}

icon={<FaTools/>}

/>





<Card

title="Anomalies"

value={

analysis.anomalies ??

realtime.anomalies ??

0

}

icon={<FaExclamationTriangle/>}

/>


</div>









{/* REPAIR DOWNLOAD */}



{

cleanFile &&


<div style={{marginTop:30}}>


<Panel title="Repair Agent Output">


<p>

Clean Dataset Generated Successfully

</p>



<p>

Removed Duplicates:

<strong>

{" "}

{

data.repair?.removed_duplicates ?? 0

}

</strong>

</p>




<p>

Rows Before:

<strong>

{" "}

{

data.repair?.original_rows ?? 0

}

</strong>

</p>



<p>

Rows After:

<strong>

{" "}

{

data.repair?.cleaned_rows ?? 0

}

</strong>

</p>






<button


onClick={()=>{


window.open(

`http://127.0.0.1:8000/download/${cleanFile}`,

"_blank"

);


}}



style={{


background:"#22c55e",

color:"white",

border:"none",

padding:"15px 25px",

borderRadius:12,

cursor:"pointer",

fontSize:16,

display:"flex",

alignItems:"center",

gap:10


}}


>


<FaDownload/>

Download Clean Dataset


</button>


</Panel>



</div>


}









{/* PIPELINE */}



<div

style={{

display:"grid",

gridTemplateColumns:

"repeat(auto-fit,minmax(300px,1fr))",

gap:20,

marginTop:30

}}

>



<Panel title="Pipeline Health">


<h2 style={{
color:"#22c55e"
}}>

{

realtime.pipeline ||

"HEALTHY"

}

</h2>



<p>

Execution Time:

<strong>

{" "}

{

data.execution_time ?? 0

}

sec

</strong>


</p>



</Panel>






<Panel title="Data Quality">


<h2>

{

analysis.quality_score ?? 0

}%

</h2>



<p>

Current dataset quality score

</p>


</Panel>



</div>









{/* AI RECOMMENDATIONS */}



<div style={{marginTop:30}}>


<Panel title="AI Recommendations">


{

analysis.recommendations?.length ?


analysis.recommendations.map(

(item:string,index:number)=>(


<p key={index}>


<FaLightbulb color="orange"/>


{" "}

{item}


</p>


)

)


:

<p>

Upload dataset to generate recommendations

</p>


}



</Panel>


</div>









{/* AGENTS */}



<div style={{marginTop:40}}>


<h2>

🤖 AI Agents Activity

</h2>




<div

style={{

display:"grid",

gridTemplateColumns:

"repeat(auto-fit,minmax(220px,1fr))",

gap:20

}}

>



{

realtime.agents ?

realtime.agents.map(

(agent:any,index:number)=>(


<Agent

key={index}

name={agent.name}

status={agent.status}

/>


)

)


:


<>

<Agent name="Data Investigator" status="Waiting"/>

<Agent name="Quality Agent" status="Waiting"/>

<Agent name="Repair Agent" status="Waiting"/>

<Agent name="Recommendation Agent" status="Waiting"/>


</>


}



</div>


</div>






</div>


</Layout>


);


}










function Card({

title,

value,

icon

}:any){


return(

<div

style={{

background:"#1e293b",

padding:20,

borderRadius:15

}}

>


<div style={{fontSize:30}}>

{icon}

</div>


<h3>

{title}

</h3>


<h2>

{value}

</h2>


</div>


);

}









function Panel({

title,

children

}:any){


return(

<div

style={{

background:"#1e293b",

padding:20,

borderRadius:15

}}

>


<h2>

{title}

</h2>


<hr/>


{children}


</div>


);

}









function Agent({

name,

status

}:{

name:string,

status:string

}){


return(

<div

style={{

background:"#1e293b",

padding:20,

borderRadius:12,

textAlign:"center"

}}

>


<h2>

<FaRobot/>

</h2>


<h3>

{name}

</h3>


<p

style={{

color:

status==="Completed"

?

"#22c55e"

:

"orange"

}}

>

● {status}

</p>


</div>


);

}