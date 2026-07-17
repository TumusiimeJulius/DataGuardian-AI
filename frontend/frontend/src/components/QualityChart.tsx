import {
LineChart,
Line,
XAxis,
YAxis,
Tooltip,
ResponsiveContainer
} from "recharts";

export default function QualityChart({data}:any){

return(

<div
style={{
background:"#1e293b",
padding:20,
borderRadius:15,
height:350
}}
>

<h2>Quality Trend</h2>

<ResponsiveContainer>

<LineChart data={data}>

<XAxis dataKey="time"/>

<YAxis/>

<Tooltip/>

<Line
type="monotone"
dataKey="score"
/>

</LineChart>

</ResponsiveContainer>

</div>

)

}