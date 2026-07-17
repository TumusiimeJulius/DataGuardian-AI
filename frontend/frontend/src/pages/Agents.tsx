import { useEffect, useState } from "react";
import * as WebSocketHook from "react-use-websocket";

import api, { WS_BASE_URL } from "../services/api";
import Layout from "../components/Layout";

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

import {
  FaRobot,
  FaDatabase,
  FaProjectDiagram,
  FaHeartbeat,
  FaBrain,
  FaTools,
  FaBell,
  FaMemory,
  FaSearch,
  FaChartLine,
  FaLightbulb,
  FaCircle,
} from "react-icons/fa";



export default function Agents(){


const [agents,setAgents]=useState<any[]>([]);

const [loading,setLoading]=useState(true);



// =================================
// WEBSOCKET REAL TIME CONNECTION
// =================================


const {

lastJsonMessage,

readyState

}=useWebSocket(

`${WS_BASE_URL}/ws/dashboard`,

{

shouldReconnect:()=>true,

reconnectInterval:3000

}

);





// =================================
// LOAD INITIAL AGENTS
// =================================


useEffect(()=>{


async function loadAgents(){


try{


const response =
await api.get("/agents");


setAgents(
response.data.agents || []
);


setLoading(false);



}catch(error){


console.error(
"Agent loading failed",
error
);


setLoading(false);


}



}


loadAgents();



},[]);







// =================================
// UPDATE AGENTS FROM WEBSOCKET
// =================================



useEffect(()=>{


if(!lastJsonMessage)
return;



const liveAgents =
(lastJsonMessage as any).agents;



if(liveAgents){


setAgents(liveAgents);


}



},[lastJsonMessage]);








const getIcon=(name:string)=>{


const n=name.toLowerCase();



if(n.includes("investigator"))
return <FaSearch color="#3b82f6" size={35}/>;



if(n.includes("pipeline"))
return <FaProjectDiagram color="#22c55e" size={35}/>;



if(n.includes("repair"))
return <FaTools color="#a855f7" size={35}/>;



if(n.includes("quality"))
return <FaDatabase color="#06b6d4" size={35}/>;



if(n.includes("root"))
return <FaLightbulb color="#f97316" size={35}/>;



if(n.includes("anomaly"))
return <FaHeartbeat color="#ef4444" size={35}/>;



if(n.includes("prediction"))
return <FaChartLine color="#0ea5e9" size={35}/>;



if(n.includes("recommendation"))
return <FaBrain color="#14b8a6" size={35}/>;



if(n.includes("alert"))
return <FaBell color="#eab308" size={35}/>;



if(n.includes("memory"))
return <FaMemory color="#8b5cf6" size={35}/>;



return <FaRobot color="#22c55e" size={35}/>;



};








if(loading){


return(

<Layout>

<h2>

Loading AI Agents...

</h2>

</Layout>

);


}








return(


<Layout>


<div

style={{

color:"white"

}}

>



<h1>

🤖 DataGuardian AI Agents

</h1>


<p

style={{

color:"#94a3b8"

}}

>

Live AI agent monitoring system

</p>





<div

style={{

marginBottom:30

}}

>


{

readyState===1?

<span style={{
color:"#22c55e"
}}>

🟢 WebSocket Connected

</span>

:

<span style={{
color:"orange"
}}>

🟠 Connecting...

</span>


}



</div>







<div

style={{

display:"grid",

gridTemplateColumns:
"repeat(auto-fit,minmax(300px,1fr))",

gap:25

}}

>



{

agents.map((agent,index)=>(


<div

key={index}

style={{

background:"#1e293b",

padding:25,

borderRadius:15,

border:"1px solid #334155"

}}

>



<div

style={{

display:"flex",

justifyContent:"space-between"

}}

>


{

getIcon(agent.name)

}



<span

style={{

color:"#22c55e"

}}

>

<FaCircle size={10}/>

{" "}

{agent.status}


</span>



</div>







<h2>

{agent.name}

</h2>



<p

style={{

color:"#cbd5e1"

}}

>


{

agent.description ||

"Autonomous AI agent managing DataGuardian operations."

}


</p>







<hr/>





<p>

<strong>

Health:

</strong>

{" "}

{

agent.health ||

"Healthy"

}


</p>




<p>

<strong>

Activity:

</strong>

</p>



<p

style={{

color:"#22c55e"

}}

>

{

agent.activity ||

"Monitoring system"

}


</p>



</div>



))


}



</div>





</div>


</Layout>


);


}