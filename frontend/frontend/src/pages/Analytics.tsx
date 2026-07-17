import {useEffect,useState} from "react";

import api from "../services/api";

import Layout from "../components/Layout";

import {
FaDatabase,
FaHeartbeat,
FaTools,
FaExclamationTriangle,
FaChartLine
} from "react-icons/fa";




export default function Analytics(){


const [data,setData]=useState<any>(null);



useEffect(()=>{


async function load(){


try{


const response =
await api.get("/analytics");


setData(
response.data
);


}

catch(error){

console.error(
"Analytics Error",
error
);

}


}



load();


},[]);






if(!data)

return(

<Layout>

<h2 style={{
color:"white"
}}>

Loading Analytics...

</h2>


</Layout>

);





return(


<Layout>


<div style={{
color:"white"
}}>


<h1>

📊 DataGuardian AI Analytics

</h1>


<p style={{
color:"#94a3b8"
}}>

AI data quality intelligence report

</p>






<div

style={{

display:"grid",

gridTemplateColumns:
"repeat(auto-fit,minmax(230px,1fr))",

gap:20

}}

>




<Card

title="Datasets"

value={data.total_datasets}

icon={<FaDatabase/>}

/>





<Card

title="Average Quality"

value={`${data.average_quality}%`}

icon={<FaHeartbeat/>}

/>






<Card

title="Duplicates"

value={data.duplicates}

icon={<FaTools/>}

/>







<Card

title="Anomalies"

value={data.anomalies}

icon={<FaExclamationTriangle/>}

/>







</div>







<div style={{
marginTop:30
}}>


<div

style={{

background:"#1e293b",

padding:25,

borderRadius:15

}}

>


<h2>

AI Repair Performance

</h2>


<hr/>


<h1 style={{
color:"#22c55e"
}}>

{data.repairs}

</h1>


<p>

Datasets automatically repaired by Repair Agent

</p>



</div>


</div>






<div style={{
marginTop:30
}}>


<div

style={{

background:"#1e293b",

padding:25,

borderRadius:15

}}

>


<h2>

Quality Overview

</h2>


<p>

Average dataset quality score:

</p>


<h1>

{data.average_quality}%

</h1>


<FaChartLine size={40}/>


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

padding:25,

borderRadius:15

}}

>


<div style={{
fontSize:35
}}>

{icon}

</div>


<h3>

{title}

</h3>


<h1>

{value}

</h1>


</div>

);


}