import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import Dashboard from './features/dashboard/pages/DashboardPage'
import DataHomePage from './features/dashboard/pages/DataHomePage'

function App() {
  return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<DataHomePage />}/>
                <Route path="/tasks" element={<Dashboard />}/>
            </Routes>
        </BrowserRouter>
  )
}

export default App
