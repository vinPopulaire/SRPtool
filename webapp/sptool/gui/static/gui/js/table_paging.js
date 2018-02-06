/*
**
**  Code used from https://codepen.io/bastony/pen/eBvOGv
**  after some alterations
**  thanks Omar!
**
**
**
*/

var $table,$n, $rowCount, $firstRow, $hasHead, $tr, $i, $ii, $j, $th, $pageCount;

// get the table element
function make_pagination() {
    $table = document.getElementById("myTable"),
        $tbody = $table.getElementsByTagName('tbody')[0],
        // number of rows per page
        $n = 10,
        // number of rows of the table
        $rowCount = $tbody.rows.length,
        // get the first cell's tag name (in the first row)
        $firstRow = $tbody.rows[0].firstElementChild.tagName,
        // boolean var to check if table has a head row
        $hasHead = $firstRow === "TH",
        // an array to hold each row
        $tr = [],
        // loop counters, to start count from rows[1] (2nd row) if the first row has a head tag
        $i,
        $ii,
        // $j = $hasHead ? 1 : 0,
        $j = 0,
        // holds the first row if it has a (<TH>) & nothing if (<TD>)
        // $th = $hasHead ? $table.rows[0].outerHTML : "";
        $th = "";
    // count the number of pages
    $pageCount = Math.ceil($rowCount / $n);
    // assign each row outHTML (tag name & innerHTML) to the array
    for ($i = $j, $ii = 0; $i < $rowCount; $i++, $ii++)
        $tr[$ii] = $tbody.rows[$i].outerHTML;
    // create a div block to hold the buttons
    if(document.getElementById("buttons")){
        ;
    } else {
        $table.insertAdjacentHTML("afterend", "<div id='buttons'></div>");
    }
    // the first sort, default page is the first one
    sort(1);
}

// ($p) is the selected page number. it will be generated when a user clicks a button
function sort($p) {
  /* create ($rows) a variable to hold the group of rows
	** to be displayed on the selected page,
	** ($s) the start point .. the first row in each page, Do The Math
	*/
  var $rows = $th,
      $s = $n * $p - $n;
  for (var $i = $s; $i < $s + $n && $i < $tr.length; $i++) $rows += $tr[$i];

  // now the table has a processed group of rows ..
  $tbody.innerHTML = $rows;
  // create the pagination buttons
  document.getElementById("buttons").innerHTML = pageButtons($pageCount, $p);
  // CSS Stuff
  document.getElementById("id" + $p).setAttribute("class", "active");
}

// ($pCount) : number of pages,($cur) : current page, the selected one ..
function pageButtons($pCount, $cur) {
  /* this variables will disable the "Prev" button on 1st page
	   and "next" button on the last one */
  var $prevDis = $cur == 1 ? "disabled" : "",
      $nextDis = $cur == $pCount ? "disabled" : "",
      /* this ($buttons) will hold every single button needed
		** it will creates each button and sets the onclick attribute
		** to the "sort" function with a special ($p) number..
		*/
      $buttons =
      "<input type='button' value='&lt;&lt; Prev' onclick='sort(" +
      ($cur - 1) +
      ")' " +
      $prevDis +
      ">";
  for ($i = 1; $i <= $pCount; $i++)
    $buttons +=
      "<input type='button' id='id" +
      $i +
      "'value='" +
      $i +
      "' onclick='sort(" +
      $i +
      ")'>";
  $buttons +=
    "<input type='button' value='Next &gt;&gt;' onclick='sort(" +
    ($cur + 1) +
    ")' " +
    $nextDis +
    ">";
  return $buttons;
}
