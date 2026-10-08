let currentFilter = "todos";
let cart = JSON.parse(localStorage.getItem("dolcesuburban_cart") || "[]");

function money(n){ return "$" + n.toLocaleString("es-CO") + " COP"; }

function renderProducts(){
  const search = document.getElementById("search").value.toLowerCase();
  const container = document.getElementById("products");
  const list = window.PRODUCTS.filter(p => {
    const matchesFilter = currentFilter === "todos" || p.category === currentFilter || p.type === currentFilter;
    const matchesSearch = p.name.toLowerCase().includes(search);
    return matchesFilter && matchesSearch;
  });
  container.innerHTML = list.map(p => `
    <article class="product">
      <div class="product-image">${p.emoji}</div>
      <div class="product-info">
        <span class="tag">${p.category} · ${p.type}</span>
        <h3>${p.name}</h3>
        <p class="price">${money(p.price)}</p>
        <p class="tag">Tallas: ${p.sizes.join(", ")}</p>
        <button class="add" onclick="addToCart(${p.id})">Agregar al carrito</button>
      </div>
    </article>`).join("");
}

document.querySelectorAll(".filter").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentFilter = btn.dataset.filter;
    renderProducts();
  });
});

function addToCart(id){
  const product = window.PRODUCTS.find(p => p.id === id);
  cart.push(product);
  saveCart();
  alert(product.name + " fue agregado al carrito.");
}

function saveCart(){
  localStorage.setItem("dolcesuburban_cart", JSON.stringify(cart));
  document.getElementById("cart-count").textContent = cart.length;
}

function openCart(){
  const modal = document.getElementById("cart-modal");
  modal.classList.add("open");
  const items = document.getElementById("cart-items");
  if(!cart.length){
    items.innerHTML = "<p>Tu carrito está vacío.</p>";
  } else {
    items.innerHTML = cart.map((p,i) => `
      <div class="cart-row">
        <span>${p.emoji} ${p.name}<br><small>${money(p.price)}</small></span>
        <button class="remove" onclick="removeFromCart(${i})">Eliminar</button>
      </div>`).join("");
  }
  document.getElementById("cart-total").textContent = money(cart.reduce((s,p)=>s+p.price,0));
}
function closeCart(){document.getElementById("cart-modal").classList.remove("open")}
function removeFromCart(i){cart.splice(i,1);saveCart();openCart()}
function checkout(){
  if(!cart.length){alert("Agrega productos antes de finalizar.");return}
  alert("¡Gracias por tu compra! En una versión conectada a pagos aquí se iniciaría el proceso de pago.");
}
function toggleChat(){document.getElementById("chatbot").classList.toggle("open")}
function addMessage(text, type){
  const box=document.getElementById("chat-messages");
  const div=document.createElement("div");
  div.className="message "+type;
  div.textContent=text;
  box.appendChild(div);
  box.scrollTop=box.scrollHeight;
}
async function sendChat(message){
  if(!message.trim()) return;
  addMessage(message,"user");
  try{
    const res=await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message})});
    const data=await res.json();
    addMessage(data.reply,"bot");
  }catch(e){
    addMessage("No pude conectarme con el servidor. Verifica que Flask esté ejecutándose.","bot");
  }
}
document.getElementById("chat-form").addEventListener("submit",e=>{
  e.preventDefault();
  const input=document.getElementById("chat-input");
  sendChat(input.value); input.value="";
});
function quickAsk(text){sendChat(text)}
renderProducts();
saveCart();
