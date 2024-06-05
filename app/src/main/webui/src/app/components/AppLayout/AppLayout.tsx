import imgAvatar from '@app/assets/bgimages/avatar-user.svg';
import logo from '@app/assets/bgimages/parasol-logo.svg';
import { IAppRoute, IAppRouteGroup, routes } from '@app/routes';
import {
  Avatar,
  Brand,
  Button,
  ButtonVariant,
  Masthead,
  MastheadBrand,
  MastheadContent,
  MastheadMain,
  MastheadToggle,
  Nav,
  NavExpandable,
  NavItem,
  NavList,
  Page,
  PageSidebar,
  PageSidebarBody,
  SkipToContent,
  Text,
  TextContent,
  TextVariants,
  Toolbar,
  ToolbarContent,
  ToolbarGroup,
  ToolbarItem
} from '@patternfly/react-core';
import { BarsIcon, BellIcon, CogIcon, QuestionCircleIcon } from '@patternfly/react-icons';
import * as React from 'react';
import { NavLink, useLocation } from 'react-router-dom';

interface IAppLayout {
  children: React.ReactNode;
}

const AppLayout: React.FunctionComponent<IAppLayout> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = React.useState(true);

  const headerToolbar = (
    <Toolbar id="toolbar" isFullHeight isStatic>
      <ToolbarContent>
        <ToolbarGroup
          variant="icon-button-group"
          align={{ default: 'alignRight' }}
          spacer={{ default: 'spacerNone', md: 'spacerMd' }}
        >
          <ToolbarItem>
            <Button aria-label="Notifications" variant={ButtonVariant.plain} icon={<BellIcon />} />
          </ToolbarItem>
          <ToolbarItem>
            <Button aria-label="Settings" variant={ButtonVariant.plain} icon={<CogIcon />} />
          </ToolbarItem>
          <ToolbarItem>
            <Button aria-label="Help" variant={ButtonVariant.plain} icon={<QuestionCircleIcon />} />
          </ToolbarItem>
        </ToolbarGroup>
        <ToolbarItem>
          <TextContent>
            <Text component={TextVariants.p} className='pf-v5-global--spacer--md'>
              Alex Garcia
            </Text>
          </TextContent>
        </ToolbarItem>
        <ToolbarItem>
          <Avatar src={imgAvatar} alt="" border='light' className='avatar'/>
        </ToolbarItem>
      </ToolbarContent>
    </Toolbar>
  );

  const Header = (
    <Masthead>
      <MastheadToggle>
        <Button variant="plain" onClick={() => setSidebarOpen(!sidebarOpen)} aria-label="Global navigation">
          <BarsIcon />
        </Button>
      </MastheadToggle>
      <MastheadMain>
        <MastheadBrand>
          <Brand src={logo} alt="Patternfly Logo" heights={{ default: '36px' }} />
        </MastheadBrand>
      </MastheadMain>
      <MastheadContent>
        {headerToolbar}
      </MastheadContent>
    </Masthead>
  );

  const location = useLocation();


  const renderNavItem = (route: IAppRoute, index: number) => (
    <NavItem key={`${route.label}-${index}`} id={`${route.label}-${index}`} isActive={route.path === location.pathname} className='navitem-flex'>
      <NavLink exact={route.exact} to={route.path} className={route.path !== '#' ? '' : 'disabled-link'}>
        {route.label}
      </NavLink>
    </NavItem>
  );

  const renderNavGroup = (group: IAppRouteGroup, groupIndex: number) => (
    <NavExpandable
      key={`${group.label}-${groupIndex}`}
      id={`${group.label}-${groupIndex}`}
      title={group.label}
      isActive={group.routes.some((route) => route.path === location.pathname)}
    >
      {group.routes.map((route, idx) => route.label && renderNavItem(route, idx))}
    </NavExpandable>
  );

  const FirstNavigation = (
    <Nav id="nav-first-simple" theme="dark">
      <NavList id="nav-list-first-simple">
        {routes.slice(0, 9).map(
          (route, idx) => route.label && (!route.routes ? renderNavItem(route, idx) : renderNavGroup(route, idx))
        )}
      </NavList>
    </Nav>
  );

  const SecondNavigation = (
    <Nav id="nav-second-simple" theme="dark">
      <NavList id="nav-second-list-simple">
        {routes.slice(9, 12).map(
          (route, idx) => route.label && (!route.routes ? renderNavItem(route, idx) : renderNavGroup(route, idx))
        )}
      </NavList>
    </Nav>
  );

  const Sidebar = (
    <PageSidebar theme="dark" >
      <PageSidebarBody isFilled>
        {FirstNavigation}
      </PageSidebarBody>
      <PageSidebarBody isFilled={false}>
        {SecondNavigation}
      </PageSidebarBody>
    </PageSidebar>
  );

  const pageId = 'primary-app-container';

  const PageSkipToContent = (
    <SkipToContent onClick={(event) => {
      event.preventDefault();
      const primaryContentContainer = document.getElementById(pageId);
      primaryContentContainer && primaryContentContainer.focus();
    }} href={`#${pageId}`}>
      Skip to Content
    </SkipToContent>
  );
  return (
    <Page
      mainContainerId={pageId}
      header={Header}
      sidebar={sidebarOpen && Sidebar}
      skipToContent={PageSkipToContent}>
      {children}
    </Page>
  );
};

export { AppLayout };
