import React, { useState } from "react";
import "./signUp.css";
import toast, { Toaster } from "react-hot-toast";
import { useSelector, useDispatch } from "react-redux";
import axios from "axios";

//imgs
import loginImg from "../../assets/images/bgs/login.png";

const SignUp = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const token = useSelector((state) => state.auth.token);
  const [isLoading, setIsLoading] = useState(false);

  const [fName, setFName] = useState("");
  const [lName, setLName] = useState("");
  const [userMail, setUserMail] = useState("");
  const [telephone, setTelephone] = useState("");
  const [userPass, setUserPass] = useState("");
  const [geoLocation, setGeoLocation] = useState([]);
  const [profileImg, setProfileImg] = useState("");

  //Formatting the string into an array
  const geoArray = {
    coordinates: geoLocation,
  };
  const coordinatesArray = geoArray.coordinates.split(',');
  const coordinatesFormatted = coordinatesArray.map(coord => parseFloat(coord));
  //--------end

  const createNewUser = async (e) => {
    e.preventDefault();
    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
        "content-type": "application/json",
      },
    };
    const data = {
      email: userMail,
      first_name: fName,
      geo: {
        coordinates: coordinatesFormatted,
        type: "Point",
      },
      image: {
        content: profileImg,
        filename: "profile-image.jpg", // Assuming this is the filename for the image
      },
      last_name: lName,
      password: userPass,
      phone_number: telephone,
      user_role: "GUEST",
    };
    try {
      const response = await axios.post(`${apiUrl}/users`, data, config);
      toast("Account Created Successfully! 🐱‍👤");
    } catch (e) {
      toast("Oops! Check all fields 🐱‍👤");
      console.log(e.message); // Corrected from 'error' to 'e'
      console.log("img", profileImg, "geo", geoLocation);
    }
  };

  return (
    <div className="wrapper row">
      <div className="wrapper-left">
        <img src={loginImg} />
        <h3 className="primary-text">
          WELCOME TO <span>GREENHUB</span>
        </h3>
        <p>
          Our eco-friendly digital haven, where sustainable living meets
          effortless shopping!
        </p>
      </div>
      <div className="wrapper-right_sign">
        <form onSubmit={createNewUser}>
          <label>
            <p>First Name</p>
            <input
              type="text"
              id="first_name"
              value={fName}
              onChange={(e) => setFName(e.target.value)}
            />
          </label>
          <label>
            <p>Last Name</p>
            <input
              type="text"
              id="last_name"
              value={lName}
              onChange={(e) => setLName(e.target.value)}
            />
          </label>
          <label>
            <p>Your Email</p>
            <input
              type="email"
              id="username"
              value={userMail}
              onChange={(e) => setUserMail(e.target.value)}
            />
          </label>
          <label>
            <p>Telephone</p>
            <input
              type="tel"
              id="phone_number"
              value={telephone}
              onChange={(e) => setTelephone(e.target.value)}
            />
          </label>
          <label>
            <p>Password</p>
            <input
              type="password"
              className="input-password"
              id="password"
              value={userPass}
              onChange={(e) => setUserPass(e.target.value)}
            />
          </label>
          <h3 className="signUp_h3">Get the most out of GreenHub 🙋‍♀️👇👇</h3>
          <label>
            <p>Geo Location</p>
            <input
              type="text"
              className="geo"
              id="coordinates"
              placeholder="ex - -178.677803,-50.2982405"
              value={geoLocation}
              onChange={(e) => setGeoLocation(e.target.value)}
            />
          </label>
          <label>
            <p>Profile Picture</p>
            <input
              type="text"
              className="image_content"
              id="content"
              placeholder="base64 str - under development"
              value={profileImg}
              onChange={(e) => setProfileImg(e.target.value)}
            />
          </label>
          <button type="submit" className="btn-login">
            Sign Up
          </button>
        </form>
      </div>
      <Toaster />
    </div>
  );
};

export default SignUp;
