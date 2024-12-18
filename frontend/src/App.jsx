import { Routes, Route, BrowserRouter} from 'react-router-dom'
import {About} from './components/About'
import {Users} from './components/Users'
import {Navbar} from './components/Navbar'

function App() {
  return (
    <BrowserRouter>
    <Navbar/>
    <div className="container p-4">
      <Routes>
        <Route path='/about' element={<About/>} />
        <Route path='/' element={<Users/>} />
      </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App
