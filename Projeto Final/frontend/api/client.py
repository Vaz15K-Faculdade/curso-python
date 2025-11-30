import requests
from typing import Dict, Any


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.current_token = None
        self.authenticated = False
        
    def set_token(self, token: str):
        """Define o token de autenticação"""
        self.current_token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        
    def clear_token(self):
        """Remove o token de autenticação"""
        self.current_token = None
        self.authenticated = False
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
            
    def _erro_conexao(self, error_str: str) -> bool:
        """Verifica se o erro é de conexão com a API"""
        return ("Max retries exceeded" in error_str or 
                "Failed to establish a new connection" in error_str or 
                "Conexão recusada" in error_str)
    
    def _menssagem_erro_conexao(self) -> str:
        """Retorna a mensagem de erro de conexão"""
        return "Não foi possível conectar-se à API, verifique se ela está online"
            
    async def registrar_usuario(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Registra um novo usuário"""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/register",
                json=user_data
            )
            if response.status_code == 201:
                return {"success": True, "user": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro no registro")
                    
                    # Email duplicado retorna 400 com "REGISTER_USER_ALREADY_EXISTS"
                    if mensagem_erro == "REGISTER_USER_ALREADY_EXISTS":
                        mensagem_erro = "Email já cadastrado no sistema"
                        
                except (ValueError, TypeError):
                    # CPF duplicado retorna 500 sem JSON válido
                    if response.status_code == 500:
                        mensagem_erro = "CPF já cadastrado no sistema"
                    elif response.status_code == 400:
                        mensagem_erro = "Dados inválidos"
                    elif response.status_code == 422:
                        mensagem_erro = "Dados inválidos. Verifique os campos obrigatórios"
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            error_str = str(e)
            if self._erro_conexao(error_str):
                return {"success": False, "error": self._menssagem_erro_conexao()}
            else:
                return {"success": False, "error": error_str}
            
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """Realiza o login do usuário"""
        try:
            login_data = {
                "username": email,
                "password": password
            }
            response = self.session.post(
                f"{self.base_url}/auth/jwt/login",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 204:
                # Login bem-sucedido, o token está nos cookies
                self.authenticated = True
                # Vamos buscar os dados do usuário
                user_data = await self.get_usuario_atual()
                if user_data["success"]:
                    return {"success": True, "user": user_data["user"]}
                else:
                    return {"success": False, "error": "Erro ao obter dados do usuário"}
            elif response.status_code == 400:
                try:
                    dados_erro = response.json()
                    detail = dados_erro.get("detail", "Email ou senha incorretos")
                    if detail == "LOGIN_BAD_CREDENTIALS":
                        mensagem_erro = "Email ou senha incorretos"
                    else:
                        mensagem_erro = detail
                except (ValueError, TypeError):
                    mensagem_erro = "Email ou senha incorretos"
                return {"success": False, "error": mensagem_erro}
            else:
                return {"success": False, "error": "Erro no servidor"}
        except Exception as e:
            error_str = str(e)
            if self._erro_conexao(error_str):
                return {"success": False, "error": self._menssagem_erro_conexao()}
            else:
                return {"success": False, "error": error_str}
            
    async def logout(self) -> Dict[str, Any]:
        """Realiza o logout do usuário"""
        try:
            response = self.session.post(f"{self.base_url}/auth/jwt/logout")
            self.clear_token()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def get_usuario_atual(self) -> Dict[str, Any]:
        """Obtém os dados do usuário atual"""
        try:
            response = self.session.get(f"{self.base_url}/users/me")
            if response.status_code == 200:
                return {"success": True, "user": response.json()}
            else:
                return {"success": False, "error": "Usuário não autenticado"}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def get_eventos(self, active_only: bool = True) -> Dict[str, Any]:
        """Obtém a lista de eventos disponíveis"""
        try:
            params = {"active_only": active_only}
            response = self.session.get(f"{self.base_url}/events/", params=params)
            if response.status_code == 200:
                return {"success": True, "events": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao buscar eventos")
                except (ValueError, TypeError):
                    mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            error_str = str(e)
            if self._erro_conexao(error_str):
                return {"success": False, "error": self._menssagem_erro_conexao()}
            else:
                return {"success": False, "error": error_str}
            
    async def criar_evento(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo evento (apenas admin/operador)"""
        try:
            response = self.session.post(
                f"{self.base_url}/events/",
                json=event_data
            )
            if response.status_code == 201:
                return {"success": True, "event": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao criar evento")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Faça login novamente."
                    elif response.status_code == 403:
                        mensagem_erro = "Acesso negado. Permissões insuficientes."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def atualizar_evento(self, event_id: int, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um evento (apenas admin/operador)"""
        try:
            response = self.session.put(
                f"{self.base_url}/events/{event_id}",
                json=event_data
            )
            if response.status_code == 200:
                return {"success": True, "event": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao atualizar evento")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Faça login novamente."
                    elif response.status_code == 403:
                        mensagem_erro = "Acesso negado. Permissões insuficientes."
                    elif response.status_code == 404:
                        mensagem_erro = "Evento não encontrado."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def deletar_evento(self, event_id: int) -> Dict[str, Any]:
        """Remove um evento (apenas admin/operador)"""
        try:
            response = self.session.delete(f"{self.base_url}/events/{event_id}")
            if response.status_code == 204:
                return {"success": True}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao remover evento")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Faça login novamente."
                    elif response.status_code == 403:
                        mensagem_erro = "Acesso negado. Permissões insuficientes."
                    elif response.status_code == 404:
                        mensagem_erro = "Evento não encontrado."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def alternar_status_evento(self, event_id: int) -> Dict[str, Any]:
        """Ativa/desativa um evento (apenas admin/operador)"""
        try:
            response = self.session.patch(f"{self.base_url}/events/{event_id}/toggle-active")
            if response.status_code == 200:
                return {"success": True, "event": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao alterar status do evento")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Faça login novamente."
                    elif response.status_code == 403:
                        mensagem_erro = "Acesso negado. Permissões insuficientes."
                    elif response.status_code == 404:
                        mensagem_erro = "Evento não encontrado."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def get_meus_ingressos(self) -> Dict[str, Any]:
        """Obtém os ingressos do usuário logado"""
        try:
            response = self.session.get(f"{self.base_url}/tickets/my-tickets/")
            if response.status_code == 200:
                return {"success": True, "tickets": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao buscar ingressos")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Faça login novamente."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"

                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def get_todos_usuarios(self) -> Dict[str, Any]:
        """Obtém a lista de todos os usuários (apenas para admins)"""
        try:
            response = self.session.get(f"{self.base_url}/users/")
            if response.status_code == 200:
                return {"success": True, "users": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao buscar usuários")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Faça login novamente."
                    elif response.status_code == 403:
                        mensagem_erro = "Acesso negado. Permissões insuficientes."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"

                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def atualizar_usuario(self, user_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um usuário (apenas para admins)"""
        try:
            response = self.session.patch(
                f"{self.base_url}/users/{user_id}",
                json=update_data
            )
            if response.status_code == 200:
                return {"success": True, "user": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao atualizar usuário")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Faça login novamente."
                    elif response.status_code == 403:
                        mensagem_erro = "Acesso negado. Permissões insuficientes."
                    elif response.status_code == 404:
                        mensagem_erro = "Usuário não encontrado."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    # Métodos para gerenciamento de lotes de ingressos
    async def get_lotes_evento(self, event_id: int) -> Dict[str, Any]:
        """Obtém os lotes de ingressos de um evento"""
        try:
            response = self.session.get(f"{self.base_url}/tickets/batches/event/{event_id}")
            if response.status_code == 200:
                return {"success": True, "batches": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao buscar lotes")
                except (ValueError, TypeError):
                    mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def criar_lote_ingresso(self, dado_lote: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo lote de ingressos"""
        try:
            response = self.session.post(
                f"{self.base_url}/tickets/batches/",
                json=dado_lote
            )
            if response.status_code == 201:
                return {"success": True, "batch": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao criar lote")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Faça login novamente."
                    elif response.status_code == 403:
                        mensagem_erro = "Acesso negado. Permissões insuficientes."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"

                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def deletar_lote_ingresso(self, batch_id: int) -> Dict[str, Any]:
        """Remove um lote de ingressos"""
        try:
            response = self.session.delete(f"{self.base_url}/tickets/batches/{batch_id}")
            if response.status_code == 204:
                return {"success": True}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao remover lote")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Faça login novamente."
                    elif response.status_code == 403:
                        mensagem_erro = "Acesso negado. Permissões insuficientes."
                    elif response.status_code == 404:
                        mensagem_erro = "Lote não encontrado."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def comprar_ingressos(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compra ingressos para um evento"""
        try:
            response = self.session.post(
                f"{self.base_url}/tickets/purchase/",
                json=ticket_data
            )
            if response.status_code == 201:
                return {"success": True, "tickets": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao comprar ingressos")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Faça login novamente."
                    elif response.status_code == 400:
                        mensagem_erro = "Ingressos indisponíveis ou dados inválidos."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def get_preco_atual(self, event_id: int) -> Dict[str, Any]:
        """Obtém o preço atual de um evento"""
        try:
            response = self.session.get(f"{self.base_url}/tickets/event/{event_id}/current-price")
            if response.status_code == 200:
                return {"success": True, "price_info": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao buscar preço")
                except (ValueError, TypeError):
                    mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    async def atualizar_lote_ingresso(self, batch_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um lote de ingressos"""
        try:
            response = self.session.put(
                f"{self.base_url}/tickets/batches/{batch_id}",
                json=update_data
            )
            if response.status_code == 200:
                return {"success": True, "batch": response.json()}
            else:
                try:
                    dados_erro = response.json()
                    mensagem_erro = dados_erro.get("detail", "Erro ao atualizar lote")
                except (ValueError, TypeError):
                    if response.status_code == 401:
                        mensagem_erro = "Não autorizado. Apenas administradores podem atualizar lotes."
                    elif response.status_code == 404:
                        mensagem_erro = "Lote não encontrado."
                    else:
                        mensagem_erro = f"Erro no servidor (código {response.status_code})"
                
                return {"success": False, "error": mensagem_erro}
        except Exception as e:
            return {"success": False, "error": str(e)}
