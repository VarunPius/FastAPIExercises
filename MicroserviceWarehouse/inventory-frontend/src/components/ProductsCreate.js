import { Wrapper } from "./Wrapper"
import { useState } from "react"
import { useNavigate } from "react-router-dom";

export const ProductsCreate = () => {
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [qty, setQuantity] = useState('');
    const navigate = useNavigate();

    const submit = async e => {
        e.preventDefault();

        await fetch('http://localhost:8000/product', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                name,
                price,
                qty
            })
        });

        await navigate(-1);
    }

    return <Wrapper>
        <form className="mt-3" onSubmit={submit}>
            <div className="form-floating pb-3">
                <input className="form-control" placeholder="Name"
                    onChange={e => setName(e.target.value)}
                />
                <label>Name</label>
            </div>
            <div className="form-floating pb-3">
                <input type="number" className="form-control" placeholder="Price"
                    onChange={e => setPrice(e.target.value)}
                />
                <label>Price</label>
            </div>
            <div className="form-floating pb-3">
                <input type="number" className="form-control" placeholder="Quantity"
                    onChange={e => setQuantity(e.target.value)}
                />
                <label>Quant</label>
            </div>

            <button className="w-100 btn btn-lg btn-primary">Submit</button>
        </form>
    </Wrapper>
}