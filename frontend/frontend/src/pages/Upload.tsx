import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api, { API_BASE_URL } from "../services/api";
import Layout from "../components/Layout";

import {
FaUpload,
FaDatabase,
FaCheckCircle,
FaDownload,
FaRobot
} from "react-icons/fa";




export default function Upload(){


const navigate = useNavigate();


const [file,setFile]=useState<File|null>(null);

const [loading,setLoading]=useState(false);

const [result,setResult]=useState<any>(null);





async function uploadDataset(){


if(!file)
return;



const formData = new FormData();


formData.append(
"file",
file
);



try{


setLoading(true);



const response =
await api.post(

"/upload",

formData,

{

headers:{

"Content-Type":
"multipart/form-data"

}

}

);





const data =
response.data;




setResult(data);




// Save report temporarily

localStorage.setItem(

"latest_report",

JSON.stringify(data)

);




// Redirect after completion

setTimeout(()=>{


navigate("/reports");


},2000);




}

catch(error){


console.error(
"Upload failed",
error
);


}

finally{


setLoading(false);


}



}





return(


<Layout>


<div

style={{

color:"white"

}}

>


<h1>

📤 Upload Dataset

</h1>



<p

style={{

color:"#94a3b8"

}}

>

Upload CSV or Excel files for AI-powered quality analysis.

</p>







<div

style={{

background:"#1e293b",

padding:30,

borderRadius:15,

marginTop:30

}}

>


<input

type="file"

accept=".csv,.xlsx,.xls"

onChange={(e)=>{


if(e.target.files)

setFile(
e.target.files[0]
);


}}

/>




<br/><br/>




<button

onClick={uploadDataset}

disabled={loading}


style={{

background:"#2563eb",

color:"white",

padding:"12px 25px",

borderRadius:10,

border:"none",

cursor:"pointer"

}}

>


{

loading ?

"🤖 AI Agents Working..."

:

"Upload & Analyze"

}


</button>



</div>







{

result &&


<div

style={{

marginTop:30,

display:"grid",

gridTemplateColumns:
"repeat(auto-fit,minmax(250px,1fr))",

gap:20

}}

>



<Card

title="Quality Score"

value={

result.summary?.quality_score+"%"

}

icon={<FaCheckCircle/>}

/>



<Card

title="Missing Values"

value={

result.summary?.missing_values

}

icon={<FaDatabase/>}

/>



<Card

title="Duplicates"

value={

result.summary?.duplicates

}

icon={<FaRobot/>}

/>



<Card

title="Anomalies"

value={

result.summary?.anomalies

}

icon={<FaRobot/>}

/>



</div>


}







{

result?.repair &&


<div

style={{

background:"#1e293b",

padding:25,

borderRadius:15,

marginTop:30

}}

>


<h2>

🧹 Repair Agent Completed

</h2>



<p>

Removed duplicates:

<strong>

{" "}

{
result.repair.removed_duplicates

}

</strong>

</p>



<p>

Original Rows:

{
result.repair.original_rows
}

</p>



<p>

Clean Rows:

{
result.repair.cleaned_rows
}

</p>






<a

href={

`${API_BASE_URL}/download/${result.repair.clean_file}`

}


style={{

display:"inline-flex",

gap:10,

alignItems:"center",

background:"#22c55e",

padding:"12px 20px",

borderRadius:10,

color:"black",

textDecoration:"none"

}}

>


<FaDownload/>

Download Clean Dataset


</a>





</div>


}






{

loading &&


<div

style={{

marginTop:30,

color:"#22c55e"

}}

>


<FaUpload/>

Uploading...


<br/>

🤖 Data Investigator Agent running

<br/>

📊 Quality Agent analyzing

<br/>

🧹 Repair Agent cleaning


</div>


}



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


<div

style={{

fontSize:30

}}

>

{icon}

</div>



<h3>

{title}

</h3>



<h2>

{value ?? 0}

</h2>



</div>


);


}