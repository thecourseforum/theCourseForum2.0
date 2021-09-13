function unsaveCourse(courseID, instructorID, id) {
    const csrftoken = getCookie("csrftoken");

    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrftoken },
        url: `/unsave_course/${courseID}/${instructorID}`
    });

    document.getElementById(`course${id}`).remove();
    document.getElementById(`saveCourseModal${id}`).remove();

    // if no more courses left
    if ($(".course-card").length === 0) {
        document.getElementById("courseToolbar").remove();
        $("#noCoursesCard").css("display", "block");
    }
}

function editCourse(courseID, instructorID, id) {
    const notes = $(`#notesField${id}`).val();
    const csrftoken = getCookie("csrftoken");

    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": csrftoken },
        url: `/save_course/${courseID}/${instructorID}/edit`,
        data: { notes: notes }
    });

    $(`#notes${id}`).text(notes);

    if ($(`#notes${id}`).height() === $("#rating").height()) {
        $(`#notes${id}`).removeClass("collapsed");
        $(`#notes${id}`).removeClass("collapsible");
    } else {
        $(`#notes${id}`).addClass("collapsed");
        $(`#notes${id}`).addClass("collapsible");
        $(`#notes${id}`).click(function() {
            $(`#notes${id}`).toggleClass("collapsed");
        });
    }
}

// Configure unsave and edit course buttons
const buttons = document.getElementsByClassName("save-btn");
for (let i = 0; i < buttons.length; i++) {
    const button = buttons[i];
    const id = button.id.substring(13); // remove "saveCourseBtn" from string
    const course = $(`#courseID${id}`).val();
    const instructor = $(`#instructorID${id}`).val();

    document.getElementById(`unsaveCourseBtn${id}`).addEventListener("click", () => unsaveCourse(course, instructor, id), false);
    document.getElementById(`saveCourseBtn${id}`).addEventListener("click", () => editCourse(course, instructor, id), false);

    // Notes collapser
    if ($(`#notes${id}`).height() > $("#rating").height()) { // check if notes longer than 1 line
        $(`#notes${id}`).addClass("collapsed");
        $(`#notes${id}`).addClass("collapsible");
        $(`#notes${id}`).click(function() {
            $(`#notes${id}`).toggleClass("collapsed");
        });
    }
}

if (buttons.length > 0) {
    // Drag and Drop
    $("#savedCoursesList").sortable();
    $("#savedCoursesList").disableSelection();

    $("#savedCoursesList").on("sortstart", function(event, ui) {
        // highlight border when dragging
        const moved = ui.item.context;
        const movedID = moved.id.substring(6); // remove "course" from string
        $(`#card${movedID}`).addClass("dragging");
    });

    $("#savedCoursesList").on("sortstop", function(event, ui) {
        // remove border highlight
        const moved = ui.item.context;
        const movedID = moved.id.substring(6); // remove "course" from string
        $(`#card${movedID}`).removeClass("dragging");
    });

    $("#savedCoursesList").on("sortupdate", function(event, ui) {
        // save course order
        const moved = ui.item.context;
        const movedID = moved.id.substring(6); // remove "course" from string
        const successor = $(`#${moved.id}`).prev("li")[0];
        const csrftoken = getCookie("csrftoken");
        let data;
        try {
            const successorID = successor.id.substring(6);
            data = {
                to_move_id: movedID,
                successor_id: successorID
            };
        } catch (error) {
            // successor ID is undefined, move to beginning of list
            data = {
                to_move_id: movedID
            };
        }

        $.ajaxSetup({
            headers: { "X-CSRFToken": csrftoken }
        });

        $.ajax({
            type: "POST",
            url: "/saved/reorder",
            data: data
        });
    });
} else {
    // show no courses card
    $("#noCoursesCard").css("display", "block");
}