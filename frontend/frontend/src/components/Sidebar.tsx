import {

  FaHome,
  FaSearch,
  FaRobot,
  FaUpload,
  FaChartLine,
  FaCog,
  FaShieldAlt,
  FaBell,
  FaDatabase,
  FaHeartbeat,
  FaDownload,
  FaFileAlt,
  FaMagic

} from "react-icons/fa";


import {
  Link,
  useLocation
} from "react-router-dom";





const menu = [


{
name:"Dashboard",
path:"/",
icon:<FaHome/>
},



{
name:"Investigation",
path:"/investigation",
icon:<FaSearch/>
},



{
name:"AI Agents",
path:"/agents",
icon:<FaRobot/>
},



{
name:"Upload Dataset",
path:"/upload",
icon:<FaUpload/>
},



{
name:"Data History",
path:"/history",
icon:<FaDatabase/>
},



{
name:"Clean Datasets",
path:"/clean",
icon:<FaDownload/>
},




{
name:"Analytics",
path:"/analytics",
icon:<FaChartLine/>
},




{
name:"AI Reports",
path:"/reports",
icon:<FaFileAlt/>
},




{
name:"AI Recommendations",
path:"/recommendations",
icon:<FaMagic/>
},





{
name:"Alerts",
path:"/alerts",
icon:<FaBell/>
},




{
name:"Settings",
path:"/settings",
icon:<FaCog/>
}



];







export default function Sidebar(){



const location = useLocation();




return(



<aside

style={{

width:260,

height:"100vh",

position:"fixed",

left:0,

top:0,

background:
"linear-gradient(180deg,#020617,#0f172a)",

color:"white",

padding:"25px 15px",

boxShadow:
"5px 0 25px rgba(0,0,0,.4)",

overflowY:"auto",

zIndex:1000

}}

>



{/* LOGO */}


<div

style={{

display:"flex",

alignItems:"center",

gap:12,

marginBottom:35,

fontSize:22,

fontWeight:"bold"

}}

>


<div

style={{

background:"#22c55e",

padding:10,

borderRadius:12,

display:"flex"

}}

>


<FaShieldAlt/>


</div>



DataGuardian AI



</div>








<nav>



{

menu.map((item)=>{


const active =
location.pathname === item.path;



return(


<Link

key={item.path}

to={item.path}



style={{


display:"flex",

alignItems:"center",

gap:15,

padding:"13px 15px",

marginBottom:8,

borderRadius:12,

textDecoration:"none",

color:"white",



background:

active

?

"linear-gradient(90deg,#2563eb,#1d4ed8)"

:

"transparent",




boxShadow:

active

?

"0 0 15px rgba(37,99,235,.5)"

:

"none",




transition:"0.3s"


}}



onMouseEnter={(e)=>{


if(!active)

e.currentTarget.style.background="#1e293b";


}}




onMouseLeave={(e)=>{


if(!active)

e.currentTarget.style.background="transparent";


}}



>


<span

style={{

fontSize:20

}}

>

{item.icon}

</span>



<span>

{item.name}

</span>



</Link>


)



})


}



</nav>









{/* PIPELINE STATUS */}



<div

style={{


position:"fixed",

bottom:25,

left:15,

width:230,

background:"#1e293b",

padding:18,

borderRadius:15,

boxShadow:
"0 0 20px rgba(0,0,0,.3)"


}}

>



<div

style={{

display:"flex",

alignItems:"center",

gap:10,

marginBottom:10

}}

>


<FaHeartbeat color="#22c55e"/>


<strong>

System Online

</strong>


</div>







<div

style={{

fontSize:13,

color:"#94a3b8"

}}

>


🟢 AI Engine Active


<br/>


🟢 Dataset Analyzer Running


<br/>


🟢 Repair Agent Ready


<br/>


🟢 History Database Connected


<br/>


🟢 WebSocket Live


</div>



</div>






</aside>


);


}