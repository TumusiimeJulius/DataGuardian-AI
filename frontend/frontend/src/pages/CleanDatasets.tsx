import {useEffect,useState} from "react";

import api, { API_BASE_URL } from "../services/api";

import Layout from "../components/Layout";



export default function CleanDatasets(){


const [files,setFiles]=useState<any[]>([]);



useEffect(()=>{


async function load(){


try{


const response =
await api.get("/history");


const data =
response.data.history || [];



setFiles(

data.filter(
(item:any)=>item.clean_file
)

);


}

catch(error){

console.log(error);

}


}



load();


},[]);






return(


<Layout>


<div style={{
color:"white"
}}>



<h1>

🧹 Clean Dataset Export

</h1>



<p style={{
color:"#94a3b8"
}}>

Files repaired by the Repair Agent

</p>





<div

style={{

display:"grid",

gridTemplateColumns:
"repeat(auto-fit,minmax(300px,1fr))",

gap:20

}}

>



{


files.map((file)=>(


<div

key={file.id}

style={{

background:"#1e293b",

padding:25,

borderRadius:15

}}

>


<h2>

{file.clean_file}

</h2>



<p>

Original:

<br/>

{file.filename}

</p>



<a

href={

`${API_BASE_URL}/download/${file.clean_file}`

}

style={{

background:"#22c55e",

padding:"10px 20px",

borderRadius:10,

color:"black",

textDecoration:"none"

}}

>

Download

</a>



</div>


))


}




</div>



</div>


</Layout>


);


}