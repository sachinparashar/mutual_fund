const menuItemNodes = document.getElementsByClassName("menu-items-wrapper");

const handleOnMenuClick = (menuItemNode) => {
  const subMenuNodes = menuItemNode.getElementsByClassName("sub-menus");

  allowSubMenuClick(subMenuNodes);

  toggleSubMenus(subMenuNodes);
};

const allowSubMenuClick = (subMenuNodes) => {
  let activeIndex = 0;
  [...subMenuNodes].forEach((element, elementIndex) => {
    element.addEventListener("click", (event) => {
      event.stopImmediatePropagation();

      filterSubMenuActiveStyle(subMenuNodes, activeIndex, elementIndex);

      // set current element clicked to activeIndex
      activeIndex = elementIndex;

      toggleSubMenuActiveStyle(subMenuNodes, elementIndex);
    });
  });
};

// filter sub menu active state
const filterSubMenuActiveStyle = (subMenuNodes, activeIndex, elementIndex) => {
  if (activeIndex !== elementIndex) {
    subMenuNodes[activeIndex]
      .getElementsByClassName("fa-solid fa-circle")[0]
      .classList.remove("sub-menus-active");
  }
};

// add or remove sub menu active state
const toggleSubMenuActiveStyle = (subMenuNodes, elementIndex) => {
  subMenuNodes[elementIndex]
    .getElementsByClassName("fa-solid fa-circle")[0]
    .classList.toggle("sub-menus-active");
};

// show or hide sub menus
const toggleSubMenus = (subMenuNodes) => {
  [...subMenuNodes].map((item) => item.classList.toggle("show-sub-menus"));
};

// menu on click event
[...menuItemNodes].forEach((menuItemNode) => {
  menuItemNode.addEventListener("click", () => handleOnMenuClick(menuItemNode));
});

const toggleTabs = (graph, tab) => {
  const graphs = document.getElementsByClassName("graphs");
  const tabs = document.getElementsByClassName("share-detail-tab");
  for (let i = 0; i < graphs.length; i++) {
    graphs[i].style.display = "none";
  }
  for (let i = 0; i < tabs.length; i++) {
    tabs[i].style.borderBottomWidth = "4px";
    tabs[i].style.borderBottomStyle = "solid";
    tabs[i].style.borderBottomColor = "transparent";
    tabs[i].style.color = "#7d7d7d";
  }
  document.getElementById(graph).style.display = "block";
  document.getElementById(tab).style.borderBottomWidth = "4px";
  document.getElementById(tab).style.borderBottomStyle = "solid";
  document.getElementById(tab).style.borderBottomColor = "#7030a0";
  document.getElementById(tab).style.color = "#7030a0";
};

const toggleMenu = () => {
  const hamburger = document.getElementById("hamburger");
  const sidebar = document.getElementsByClassName("sidebar-menu")[0];

  hamburger.addEventListener("click", () => {
    if (sidebar.style.display === "block") {
      sidebar.style.display = "none";
    } else {
      sidebar.style.display = "block";
    }
  });
};

const closeMenu = () => {
  const close = document.getElementById("close-menu");
  const sidebar = document.getElementsByClassName("sidebar-menu")[0];

  close.addEventListener("click", () => {
    sidebar.style.display = "none";
  });
};
