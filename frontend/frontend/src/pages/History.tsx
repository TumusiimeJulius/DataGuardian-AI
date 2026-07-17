import { useEffect, useState } from "react";

import api, { API_BASE_URL } from "../services/api";

import Layout from "../components/Layout";

import {
  FaDatabase,
  FaDownload,
  FaSync,
  FaChartLine,
  FaExclamationTriangle,
  FaCopy
} from "react-icons/fa";





export default function History(){



const [history,setHistory]=useState<any[]>([]);

const [loading,setLoading]=useState(true);

const [error,setError]=useState("");






// =====================================
// LOAD HISTORY
// =====================================


async function loadHistory(){


try{


setLoading(true);


const response = await api.get(
"/history"
);



setHistory(

response.data.history ||

response.data ||

[]

);



setError("");



}

catch(error){


console.error(
"History loading error",
error
);


setError(
"Failed to load dataset history"
);


}

finally{


setLoading(false);


}


}







useEffect(()=>{


loadHistory();


},[]);









if(loading){


return(

<Layout>


<h2 style={{
color:"white"
}}>

Loading Dataset History...

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






{/* HEADER */}



<div

style={{

display:"flex",

justifyContent:"space-between",

alignItems:"center",

marginBottom:30

}}

>


<div>

<h1>

📚 Dataset Investigation History

</h1>


<p style={{

color:"#94a3b8"

}}>

Previously analyzed datasets stored in SQLite

</p>

</div>






<button

onClick={loadHistory}

style={{

background:"#2563eb",

color:"white",

border:"none",

padding:"12px 18px",

borderRadius:10,

cursor:"pointer",

display:"flex",

gap:10,

alignItems:"center"

}}

>

<FaSync/>

Refresh

</button>



</div>









{

error &&


<div

style={{

background:"#7f1d1d",

padding:15,

borderRadius:10

}}

>

{error}

</div>



}









{

history.length===0 ?


<div

style={{

background:"#1e293b",

padding:30,

borderRadius:15

}}

>


<h2>

No Dataset History Found

</h2>


<p>

Upload a dataset to create your first AI investigation record.

</p>


</div>



:





<div

style={{

display:"grid",

gridTemplateColumns:

"repeat(auto-fit,minmax(320px,1fr))",

gap:25

}}

>





{

history.map((item)=>(


<div

key={item.id}

style={{

background:"#1e293b",

padding:25,

borderRadius:18,

border:"1px solid #334155"

}}

>





<h2>

📄 {item.filename}

</h2>






<div

style={{

display:"flex",

gap:10,

alignItems:"center"

}}

>

<FaChartLine color="#22c55e"/>


<p>

Quality Score:

<strong>

{" "}

{item.quality_score ?? 0}%

</strong>


</p>


</div>









<p>

<FaDatabase/>

{" "}

Missing Values:

<strong>

{" "}

{item.missing_values}

</strong>


</p>









<p>

<FaCopy/>

{" "}

Duplicates:

<strong>

{" "}

{item.duplicates}

</strong>


</p>









<p>

<FaExclamationTriangle color="orange"/>

{" "}

Anomalies:

<strong>

{" "}

{item.anomalies}

</strong>


</p>









<p

style={{

color:"#94a3b8"

}}

>

Uploaded:

<br/>


{

item.uploaded_at ?

new Date(
item.uploaded_at
).toLocaleString()

:

"Unknown"

}



</p>











{

item.clean_file &&



<a

href={

`${API_BASE_URL}/download/${item.clean_file}`

}

target="_blank"

rel="noreferrer"

style={{

display:"flex",

alignItems:"center",

gap:10,

background:"#22c55e",

color:"white",

padding:"12px",

borderRadius:10,

textDecoration:"none",

justifyContent:"center"

}}

>


<FaDownload/>

Download Clean Dataset


</a>



}





</div>



))


}



</div>



}





</div>


</Layout>


);


}