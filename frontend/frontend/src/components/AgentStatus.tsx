interface Props {
    name: string;
    status: string;
    color: string;
}

export default function AgentStatus({
    name,
    status,
    color
}: Props){

return(

<div
style={{
background:"#1e293b",
padding:20,
borderRadius:15
}}
>

<h3>{name}</h3>

<div
style={{
marginTop:15,
color
}}
>

● {status}

</div>

</div>

)

}