import React, { useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import { Provider } from "react-redux";
import { useSelector } from "react-redux";
import { setToken, setUser } from "./redux/slices/authSlice";

import { store } from "./redux/store";

//Customer
import Home from "./Pages/Customer/Home/Home";
import Nav from "./Pages/Customer/Nav/Nav";
//Admin
import DashNav from "./Pages/Admin/DashNav/DashNav";
import Dashboard from "./Pages/Admin/Dashboard/Dashboard";

const App = () => {
  //Checks user role on Login
  const ProtectedRoutes = ({
    protectedComponent,
    guestComponent = null,
    user,
  }) => {
    if (!user) {
      return <Login />;
    }
    if (user && user.user_role == "ADMIN") {
      return protectedComponent;
    }

    return guestComponent;
  };

  const user = useSelector((state) => state.auth.user);

  useEffect(() => {
    let authUser = localStorage.getItem("authUser");
    let authToken = localStorage.getItem("accessToken");
    if (authUser) {
      authUser = JSON.parse(authUser);
      store.dispatch(setUser(authUser));
      store.dispatch(setToken(authToken));
    }
  }, []);

  console.log("user", user);
  return (
    <>
      {user ? (user.user_role == "ADMIN") ? <DashNav /> : <Nav /> : ""}
      <Routes>
         <Route path="/" element={user ? (user.user_role == "ADMIN") ? <Dashboard /> : <Home /> : <Home />} />
      </Routes>
    </>
  );
};

export default App;
