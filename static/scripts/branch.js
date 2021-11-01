
    function makeBranchDetail(element,baseBranch,branchdetail) {
        element.parentNode.removeChild(element);
        let targetBranch=document.getElementById("select"+baseBranch);
        let branchList=document.getElementById("branchList");
        //create node
        let newNode=targetBranch.cloneNode(true);
        newNode.id='select'+baseBranch+branchdetail;
        newNode.classList.add('bg-secondary');

        newNode.querySelector('.col-7').innerHTML=
            "<p class='text-white'>"+branches[baseBranch].name+" with " + branches[branchdetail].name+" branch detail</p>";
        newNode.querySelector('.col-5').classList.add("align-items-end");
        newNode.querySelector('.col-5').innerHTML=
            `<button type="button" class="btn btn-danger" onclick="removeBranchDetail(this,'${baseBranch}','${branchdetail}')">Remove</button>`;
        branchList.insertBefore(newNode,targetBranch);
    }

    //return branch detail to basebranch selection item
    function removeBranchDetail(element,baseBranch,branchDetail) {
        let detailDropdown=document.querySelector(`#select${baseBranch}`).querySelector('.dropdown-menu');
        detailDropdown.innerHTML+=
            `<li id="branchDetail${baseBranch}${branchDetail}" onclick="makeBranchDetail(this,'${baseBranch}','${branchDetail}')"><a class="dropdown-item" href="#">${branchDetail}</a></li>`;
        let branchList=document.querySelector('#branchList');
        branchList.removeChild(branchList.querySelector(`#select${baseBranch}${branchDetail}`));
    }


    function addBRADSO(baseBranch) {
        let targetBranch=document.getElementById("select"+baseBranch);
        let branchList=document.getElementById("branchList");
        //create node
        let newNode=targetBranch.cloneNode(true);
        newNode.id='select'+baseBranch+'BRADSO';
        newNode.classList.add('bg-secondary');


        newNode.querySelector('.col-7').innerHTML=
            `<p class='text-white'>${branches[baseBranch].name} BRADSO</p>`;
        newNode.querySelector('.col-5').classList.add("align-items-end");
        newNode.querySelector('.col-5').innerHTML=
            `<button type="button" class="btn btn-danger" onclick="removeBRADSO('${baseBranch}')">Remove</button>`;
        branchList.insertBefore(newNode,targetBranch);

        let bradsoCheck=document.querySelector(`#flexSwitch${baseBranch}`);
        bradsoCheck.onclick= function() { removeBRADSO(baseBranch) }

    }

    function removeBRADSO(baseBranch) {
        let bradsoCheck=document.querySelector(`#flexSwitch${baseBranch}`);
        bradsoCheck.checked=false;
        let branchList=document.querySelector('#branchList');
        branchList.removeChild(branchList.querySelector(`#select${baseBranch}BRADSO`));
        bradsoCheck.onclick= function() { addBRADSO(baseBranch) }
    }

    // grab everything from fields, send to generation endpoint
    // return pdf to user
    function downloadMemo() {
        // get data
        let first = document.querySelector("#txtFirst").value;
        let last = document.querySelector("#txtLast").value;
        let email = document.querySelector("#txtEmail").value;
        let company = document.querySelector("#lstCompany").value;

        // validate

        if(first.length===0 || last.length===0) {
            alert("Full name isn't filled out. Put your first and last name in.")
            return;
        }
        if(email.length===0 || !email.includes("westpoint.edu")) {
            alert("Please put in a valid @westpoint.edu email.");
            return;
        }

        let listArray = Array.from(branchList.children);
        prefs = [];
        listArray.forEach((item) => {
            prefs.push(item.querySelector("p").textContent)
        });

        var customData= {
            "first":first,
            "last":last,
            "email":email,
            "company":company,
            "prefs":prefs
        }

        redirectPost("/genDoc", customData)


    // https://stackoverflow.com/questions/19064352/how-to-redirect-through-post-method-using-javascript/38445519
    // makes a form programmatically and adds all desired data to fake form
    function redirectPost(url, data) {
        var form = document.createElement('form');
        document.body.appendChild(form);
        form.method = 'POST';
        form.action = url;
        for (var name in data) {
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = name;
            input.value = data[name];
            form.appendChild(input);
        }
        form.submit();
    }
}
