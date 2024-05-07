import React from "react";
import "./categories.css";
import { NavLink } from "react-router-dom";
//Imgs
import menu from "../../assets/images/icons/menu.png";
import zeroWaste from "../../assets/images/icons/zero.png";
import ecoKitchen from "../../assets/images/icons/kitchen.png";
import beauty from "../../assets/images/icons/beauty.png";

const Categories = () => {
  return (
    <div className="categories__container">
      <div className="categories__container-categories">
        <div className="categories__header">
          <img src={menu} />
          <h4>Categories</h4>
        </div>
        <div className="categories__content">
          <ul>
            <NavLink to="/zero-waste">
              <li>
                <img src={zeroWaste} />
                <h4>Zero Waste</h4>
              </li>
            </NavLink>
            <NavLink to="/eco-kitchen">
              <li>
                <img src={ecoKitchen} />
                <h4>Eco Kitchen</h4>
              </li>
            </NavLink>
            <NavLink to="/natural-beauty">
              <li>
                <img src={beauty} />
                <h4>Natural Beauty</h4>
              </li>
            </NavLink>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Categories;
