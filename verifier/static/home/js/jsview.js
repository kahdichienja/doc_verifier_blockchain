let sendAsync = document.querySelectorAll("#sendAsync");

sendAsync.forEach(sendAsyncReq => {
    sendAsyncReq.addEventListener("click", event => {
        let attr = event.target.parentElement.previousElementSibling.id;

        let apiendpoint = `/drive/user/${attr}`;

        var xhr = new XMLHttpRequest();
        xhr.open("GET", apiendpoint, true);

        xhr.onload = function() {
            if (this.status == 200) {
                var userfile = JSON.parse(this.responseText);
                let output = `
                        <div class="modal-body mb-0 p-0">
                            <div class="modal-header light-blue darken-2 white-text">
                                <h4 class="title">
                                    <i class="fas fa-file-upload"></i>
                                    View ${userfile.file_name}
                                </h4>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <ul class="list-group list-group-flush text-center">
                                <ul class="list-group">
                                    <li class="list-group-item">
                                        <div class="view overlay">
                                            <p>
                                                <img class="card-img-top" src="/assests/img/icons/${userfile.file_type}.png"
                                                    style="height: 4rem; width: 4rem;">
                                            </p>
                                            <a href="#!">
                                                <div class="mask rgba-white-slight"></div>
                                            </a>
                                        </div>
    
                                        ${userfile.user_define_file_name}
                                    </li>
                                </ul>
                            </ul>
                        </div>
                        `;
                document.getElementById("asyncuserfileview").innerHTML = output;
            }
        };
        xhr.send();
    });
});


let fetchtAsyncEdit = document.querySelectorAll("#sendAsyncEdit");

fetchtAsyncEdit.forEach(sendAsyncReq => {
    sendAsyncReq.addEventListener("click", event => {
        let attr = event.target.parentElement.previousElementSibling.id;

        let apiendpoint = `/drive/user/${attr}`;
        fetch(apiendpoint).then((res) => res.json())
        .then((data) => {
            let output = `
                <!--Body-->
                <div class="modal-body mb-0 p-0">
                    <div class="modal-header light-blue darken-3 white-text">
                        <h4 class="title">
                        <img 
                            class="card-img-top" 
                            src="/assests/img/icons/${data.file_type}.png"
                            style="height: 4rem; width: 4rem;"
                        > 
                            Edit ${data.user_define_file_name}
                        </h4>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span
                                aria-hidden="true">&times;</span></button>
                    </div>

                    <div class="container">
                        <input type="text" name="user_id" value="{{ Auth::user()->id }}" hidden>
                        <div class="md-form">
                            <select class="mdb-select md" name="folder_id" required>
                                <option disabled selected>Move This File To</option>
                                @foreach ($userfolders as $userfolder)
                                    <option value="{{ $userfolder->id }}">{{ $userfolder->folder_name }}</option>
                                @endforeach
                            </select>
                        </div>
                        <div class="file-field md-form">
                            <a class="btn-floating purple-gradient mt-0 float-left">
                                <i class="fas fa-cloud-upload-alt" aria-hidden="true"></i>
                                <input type="file" required>
                            </a>
                            <div class="file-path-wrapper">
                                <input class="file-path validate" type="text" placeholder="${data.file_name}">
                            </div>
                        </div>
                        <div class="md-form">
                            <input type="text" name="user_define_file_name" id="user_define_file_name" value="${data.user_define_file_name}" class="form-control" required>
                        </div>
                        <div class="md-form">
                            <input type="submit"  value=" Update :${data.user_define_file_name}" class="btn purple-gradient btn-rounded">
                        </div>
                    </div>
                </div>
                `;
                document.getElementById("asyncuserfile").innerHTML = output;
        })
        .catch((err) => console.log(err))
    });
});


let sendAsyncViewFolderFile =  document.querySelectorAll('#sendAsyncViewFolderFile')
sendAsyncViewFolderFile.forEach(sendAsyncReq => {
    sendAsyncReq.addEventListener("click", event => {
        let attr = event.target.parentElement.previousElementSibling.id;

        let apiendpoint = `/drive/sendAsync/${attr}`;
        fetch(apiendpoint).then((res) => res.json())
        .then((data) => {
            let output = ``;
            
            let filesinafolder = data[0]//gives the files in a folder
            let foldername = data[1]//gives the folder

            for (var i in filesinafolder) {
                // output += `${filesinafolder[i].file_name}`
                output += `
                <tr>
                    <td>
                        <a href="" class="text-primary">
                            <img src="{{ asset('assests/img/nofile.png') }}" style="height: 1.5rem" alt="">
                        </a>
                    </td>
                    <td>


                    </td>
                    <td>me</td>
                    <td></td>
                    <td></td>
                    <td>

                    </td>
                </tr>
                `

            }
            // console.log(foldername.folder_name)//gives the 
            document.getElementById("ViewFolderFile").innerHTML = output;
            
            
            
        })
        .catch((err) => console.log(err))
    });
});