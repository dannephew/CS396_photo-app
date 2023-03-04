const openModal = ev => {
    ev.preventDefault();
    console.log('open!');
    document.querySelector('.modal-bg').classList.remove('hidden');
    document.querySelector('.close').focus();
}

const closeModal = ev => {
    //buttons might trigger refresh, so just tells you to not do default
    ev.preventDefault();
    console.log('close!');
    //finds div tag, then adds hidden
    document.querySelector('.modal-bg').classList.add('hidden');
    document.querySelector('.open').focus();
};
