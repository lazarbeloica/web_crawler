webpackJsonp([50],{0:function(e,n,r){e.exports=r(436)},436:function(e,n,r){var a,t,i,s,o,c;a=r(2),i=r(3),t=r(11),s=r(7),o=r(12),c=r(5),r(13),ds.define("recommendations",function(e){var n,r,l,d,m;return d=e("ready"),n=c.getUrl,r=new t(function(e){var n,r;if(n=a("#recs_slider").get(0))return r=function(){return c.isElementInViewport(n)},r()?e(n):a(window).on("scroll.lazy-recommendations",i.throttle(function(){r()&&(e(n),a(window).off("scroll.lazy-recommendations"))},200))}),m=function(){var e,n,r,t,i;if(n="<!--lazy",i="lazy-->",e=a("#recs_slider"),r=e.html(),t=r.indexOf(n)>=0&&r.indexOf(i)>=0)return e.html(e.html().replace(n,"").replace(i,""))},l=function(){var e,r,t,i;if(r=a(".recommendations"),r.length)return t=r.find("#recs_slider"),e=r.find(".cards"),i=e.find(".card_large").outerWidth(!0),e.css("width",e.data("num-recs")*i),t.lazyGallery({has3d:o.has3d(),isMobile:o.isMobile,snapToSlide:!1,slideContainerClass:".cards",slideClass:".card_large",slideCount:e.data("num-recs"),advance:5,resize:!1,get:function(r){var i,o,c,l,d,m,u,f;l=s["recommendations/_macro:pagetype"],m=s["recommendations/_macro:sellerid"],u=s["recommendations/_macro:sellerUsername"],f=s["recommendations/_macro:sourceIds"],o=t.data("ev"),c=r||1,i={type:l,page:c,ev:o},m&&(i.seller=m),f&&(i.ids=JSON.stringify(f)),d="seller"===l?"/seller/"+u+"/recs":"/release/recs/"+s["recommendations/_macro:pageid"],a.get(n(d),i,function(n){return e.append(n)})}})},d(function(){return r.then(function(){return m(),l()})})})}});
//# sourceMappingURL=recommendations.js.map