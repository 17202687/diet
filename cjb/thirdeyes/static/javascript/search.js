function filter() 
{
  let search = document.getElementById("search").value.toLowerCase();
  let listInner = document.getElementsByClassName("listInner");

  for (let i = 0; i < listInner.length; i++) 
  {
    kcal = listInner[i].getElementsByClassName("kcal");
    menu = listInner[i].getElementsByClassName("menu");
    if (kcal[0].innerHTML.toLowerCase().indexOf(search) != -1 ||
        menu[0].innerHTML.toLowerCase().indexOf(search) != -1
      )
    {
      listInner[i].style.display = "flex"
    } 
    else 
    {
      listInner[i].style.display = "none"
    }
  }
}