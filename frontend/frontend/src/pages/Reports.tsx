import Layout from "../components/Layout";


export default function Reports(){


const report =
JSON.parse(

localStorage.getItem(
"latest_report"
)

|| "{}"

);



return(

<Layout>


<div style={{
color:"white"
}}>


<h1>

📊 AI Investigation Report

</h1>



<div

style={{

background:"#1e293b",

padding:30,

borderRadius:15

}}

>


<h2>

Dataset:

{report.filename}

</h2>




<h3>

Data Quality:

{report.summary?.quality_score}%

</h3>



<p>

Missing Values:

{report.summary?.missing_values}

</p>




<p>

Duplicates:

{report.summary?.duplicates}

</p>




<p>

Anomalies:

{report.summary?.anomalies}

</p>




<h2>

🤖 AI Agents Completed

</h2>



<ul>

{

report.agents?.map(

(agent:any,index:number)=>(

<li key={index}>

{agent.name}

-

{agent.status}

</li>

)

)

}

</ul>



</div>


</div>


</Layout>


);


}