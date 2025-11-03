import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

const App = () => {
  return (
   <BrowserRouter>
   <Routes>
    <Route path='/' element={<Home/>}  ></Route>
    <Route path='/cart' element={<Cart/>}  ></Route>
    <Route path='/login' element={<Login/>} ></Route>
    <Route path='/products' element={<Products/>} ></Route>
    <Route path='/wishlist' element={<Wishlist/>} ></Route>
    
   </Routes>
   
   </BrowserRouter>
  )
}

export default App
