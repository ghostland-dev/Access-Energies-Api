from fastapi import Depends, FastAPI, HTTPException, status, Request

app = FastAPI(  
    title='Voltaria API Energies DATA',
    description="Une api pour récoler les données de marcher "
    )
