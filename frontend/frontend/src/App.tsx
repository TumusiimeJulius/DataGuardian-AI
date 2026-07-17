import { BrowserRouter, Routes, Route } from "react-router-dom";


import Dashboard from "./pages/Dashboard";
import Investigation from "./pages/Investigation";
import Agents from "./pages/Agents";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";
import Upload from "./pages/Upload";

import History from "./pages/History";
import CleanDatasets from "./pages/CleanDatasets";
import Reports from "./pages/Reports";




export default function App() {


return (


<BrowserRouter>


<Routes>



{/* =========================
    MAIN DASHBOARD
========================= */}


<Route

path="/"

element={<Dashboard />}

/>






{/* =========================
    DATA UPLOAD
========================= */}


<Route

path="/upload"

element={<Upload />}

/>






{/* =========================
    INVESTIGATION
========================= */}


<Route

path="/investigation"

element={<Investigation />}

/>







{/* =========================
    AI AGENTS
========================= */}


<Route

path="/agents"

element={<Agents />}

/>







{/* =========================
    DATA HISTORY
========================= */}


<Route

path="/history"

element={<History />}

/>








{/* =========================
    CLEAN DATA EXPORT
========================= */}


<Route

path="/clean"

element={<CleanDatasets />}

/>








{/* =========================
    AI REPORTS
========================= */}


<Route

path="/reports"

element={<Reports />}

/>







{/* =========================
    ANALYTICS
========================= */}


<Route

path="/analytics"

element={<Analytics />}

/>







{/* =========================
    SETTINGS
========================= */}


<Route

path="/settings"

element={<Settings />}

/>






{/* =========================
    FALLBACK
========================= */}


<Route

path="*"

element={<Dashboard />}

/>



</Routes>


</BrowserRouter>


);


}