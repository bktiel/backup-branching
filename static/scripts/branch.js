
    function makeBranchDetail(element,baseBranch,branchdetail) {
        element.parentNode.removeChild(element);
        let targetBranch=document.getElementById("select"+baseBranch);
        let branchList=document.getElementById("branchList");
        //create node
        let newNode=targetBranch.cloneNode(true);
        newNode.id='select'+baseBranch+branchdetail;
        newNode.classList.add('bg-secondary');

        newNode.querySelector('.col-7').innerHTML=
            "<p class='text-white'>"+baseBranch+" with branch detail " + branchdetail+"</p>";
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
            `<p class='text-white'> ${baseBranch} BRADSO</p>`;
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
