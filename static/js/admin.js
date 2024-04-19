function loadPage(page) {
    fetch(page)
    .then(response => response.text())
    .then(html => {
        // 将 HTML 加载到 content 元素中
        document.getElementById('content').innerHTML = html;

        // 查找动态加载的 JavaScript 文件
        const scriptTags = document.getElementById('content').getElementsByTagName('script');
        // 循环遍历每个找到的 script 标签
        for (let i = 0; i < scriptTags.length; i++) {
            const src = scriptTags[i].src; // 获取 script 标签的 src 属性
            if (src) {
                // 如果存在 src 属性，加载外部 JavaScript 文件
                const script = document.createElement('script');
                script.src = src;
                document.body.appendChild(script); // 将新创建的 script 标签添加到页面中
            } else {
                // 如果不存在 src 属性，说明是内联的 JavaScript 代码，将其保存到一个函数中
                const scriptText = scriptTags[i].innerHTML.trim();
                if (scriptText) {
                    const scriptFunc = new Function(scriptText);
                    scriptFunc();
                }
            }
        }

        // 在动态加载完 JavaScript 后，手动调用一个初始化函数
    })
    .catch(error => console.error('页面加载失败', error));
}


const menuItems = document.querySelectorAll('.sidebar ul li');

menuItems.forEach(item => {
    item.addEventListener('click', function() {
        menuItems.forEach(i => i.classList.remove('active'));
        this.classList.add('active');
    });
});

window.addEventListener('load', function() {
    document.getElementById('userstatics').click();
});