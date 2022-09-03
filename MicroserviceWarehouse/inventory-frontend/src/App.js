import { Products } from "./components/Products";
import { ProductsCreate } from "./components/ProductsCreate";
import { Orders } from "./components/Orders";
import {BrowserRouter, Routes, Route} from 'react-router-dom'

function App() {
  return <BrowserRouter>
    <Routes>
      <Route path="/" element={<Products/>} />
      <Route path="/create" element={<ProductsCreate/>}></Route>
      <Route path="/orders" element={<Orders/>}></Route>
    </Routes>
  </BrowserRouter>;
}

export default App;
