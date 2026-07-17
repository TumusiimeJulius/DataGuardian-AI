import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

export default function Layout({
  children,
}: {
  children: React.ReactNode;
}) {

  return (

    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        background: "#0f172a",
      }}
    >


      {/* SIDEBAR */}

      <Sidebar />



      {/* MAIN CONTENT */}

      <main

        style={{

          marginLeft: 260,

          width: "calc(100% - 260px)",

          minHeight: "100vh",

          background:"#0f172a",

          transition:"all .3s ease",

        }}

      >



        {/* TOP NAVBAR */}

        <Navbar />




        {/* PAGE CONTENT */}

        <section

          style={{

            padding:"30px",

            color:"white",

            maxWidth:"1600px",

            margin:"auto",

          }}

        >

          {children}


        </section>



      </main>


    </div>

  );

}