import React from 'react'
import { NavLink } from 'react-router-dom'
import{ ShoppingBagIcon } from '@mui/icons-material/ShoppingBag';

const Navbar = () => {




  return (
    <div>
      <NavLink  to="/products" >
      <ShoppingBagIcon/>
      </NavLink>
    </div>
  )
}

export default Navbar
