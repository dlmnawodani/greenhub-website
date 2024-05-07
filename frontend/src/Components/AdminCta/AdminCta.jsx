import React from 'react';
import "./adminCta.css";

const AdminCta = ({bgColor, ctaName}) => {
  return (
    <div className='adminCta__container' style={{backgroundColor: bgColor}}>
      <h3>{ctaName}</h3>
    </div>
  )
}

export default AdminCta
