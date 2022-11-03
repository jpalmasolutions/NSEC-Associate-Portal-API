/*//container & listItems
const paginatedList = document.getElementById("page-container");
const listItems = document.getElementsByClassName("profile-wrapper");


//footer buttons
const paginationNumbers = document.getElementById("pagination-numbers");
const nextButton = document.getElementById("next-button");
const prevButton = document.getElementById("prev-button");

const paginationLimit = 200;
const pageCount = Math.ceil(listItems.length / paginationLimit);
let currentPage;


*/

const paginationNumbers = document.getElementById("pagination-numbers");
const paginatedList = document.getElementById("page-container");
const listItems = document.getElementsByClassName("profile-wrapper");
const nextButton = document.getElementById("next-button");
const prevButton = document.getElementById("prev-button");

const paginationLimit = 10;
const pageCount = Math.ceil(listItems.length / paginationLimit);
let currentPage;

const appendPageNumber = (index) => {
    const pageNumber = document.createElement("button");
    pageNumber.className = "pagination-number ";
    pageNumber.innerHTML = index;
    pageNumber.setAttribute("page-index", index);
    pageNumber.setAttribute("aria-label", "Page " + index);
   
    paginationNumbers.appendChild(pageNumber);
  };
   
  const getPaginationNumbers = () => {
    for (let i = 1; i <= pageCount; i++) {
      appendPageNumber(i);
    }
  };

  const setCurrentPage = (pageNum) => {
    currentPage = pageNum;
    

    handleActivePageNumber();
 
    const prevRange = (pageNum - 1) * paginationLimit;
    const currRange = pageNum * paginationLimit;
   
    Array.from(listItems).forEach((item, index) => {
      item.classList.add("hidden");
      if (index >= prevRange && index < currRange) {
        item.classList.remove("hidden");
      }
    });
  };

  const handleActivePageNumber = () => {

    //send user to top of page 
    window.scrollTo(0, 0);

    //set up current active page 
    document.querySelectorAll(".pagination-number").forEach((button) => {
      button.classList.remove("active");
       
      const pageIndex = Number(button.getAttribute("page-index"));
      if (pageIndex == currentPage) {
        button.classList.add("active");
        //button.classList.remove("hidden");
      }
    });
  };

  window.addEventListener("load", () => {
    getPaginationNumbers();
    setCurrentPage(1);
    document.querySelectorAll(".pagination-number").forEach((button) => {
        const pageIndex = Number(button.getAttribute("page-index"));
     
        if (pageIndex) {
          button.addEventListener("click", () => {
            setCurrentPage(pageIndex);
          });
        }
      });
  });

/*
var clientCount = document.getElementsByClassName('profile-wrapper');
var countElem = document.getElementById('count');
*/
