export default function PipelineFlow(){

const nodes=[
"Source",
"DataHub",
"Pipeline",
"Quality",
"Repair",
"Prediction",
"Dashboard"
]

return(

<div
style={{
background:"#1e293b",
padding:20,
borderRadius:15
}}
>

<h2>Pipeline Flow</h2>

<div
style={{
display:"flex",
justifyContent:"space-between",
marginTop:30
}}
>

{nodes.map(node=>(

<div
key={node}
style={{
textAlign:"center"
}}
>

<div
style={{
width:60,
height:60,
borderRadius:"50%",
background:"#2563eb",
margin:"auto"
}}
/>

<p>{node}</p>

</div>

))}

</div>

</div>

)

}