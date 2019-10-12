import React from "react";
import { Route, Switch, withRouter } from "react-router-dom";
import classnames from "classnames";
import useStyles from "./styles";
import Header from "../Header/Header";
import Sidebar from "../Sidebar/Sidebar";
import { useLayoutState } from "../../context/LayoutContext";
import Default from "../../pages/default/Default";
import Greeter from "../../pages/sample/Greeter";
import HelloMessage from "../../pages/sample/HelloMessage";

function Layout(props) {
  const classes = useStyles();
  const layoutState = useLayoutState();

  return (
    <div className={classes.root}>
        <>
          <Header />
          <Sidebar />
          <div
            className={classnames(classes.content, {
              [classes.contentShift]: layoutState.isSidebarOpened,
            })}
          >
            <div className={classes.fakeToolbar} />
            <Switch>
              <Route path="/app/default" component={Default} />
              <Route path="/app/greeter" component={Greeter} />
              <Route path="/app/hellomessage" component={HelloMessage} />
            </Switch>
          </div>
        </>
    </div>
  );
}

export default withRouter(Layout);
