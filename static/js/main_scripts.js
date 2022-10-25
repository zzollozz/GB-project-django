$( document ).on( 'click', '.category a', function(event) {
    if (event.target.hasAttribute('href')) {
        var link = event.target.href + 'ajax/';
        var link_array = link.split('/');
        if (link_array[3] == 'products') {
            fetch(link).then((response)=> {
            let json = response.json()
            return json
        }).then(data=>{
            $('.details').html(data.result);
        })
            event.preventDefault();
        }
    }
});